import itertools
import logging
from itertools import permutations

import numpy as np
from feynml import Point, Propagator

from pyfeyn2.interface.dot import dot_to_positions, feynman_to_dot


# from https://stackoverflow.com/a/9997374
def ccw(A, B, C):
    return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)


# Return true if line segments AB and CD intersect
def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


def require_xy(points):
    # check if a vertex or leg is missing a x or y position
    for v in points:
        if v.x is None:
            raise Exception(f"Vertex or leg {v} is missing x position.")
        if v.y is None:
            raise Exception(f"Vertex or leg {v} is missing y position.")


def _compute_number_of_intersects(fd):
    """
    Computes the number of crossed propagators/legs in a Feynman diagram
    """
    # check if a vertex or leg is missing a x or y position
    require_xy(points)
    points = [*fd.vertices, *fd.legs]
    lines = []
    for p in fd.propagators:
        src = fd.get_point(p.source)
        tar = fd.get_point(p.target)
        lines.append([src, tar])
    for l in fd.legs:
        if l.is_incoming():
            src = Point(l.x, l.y)
            tar = fd.get_point(l.target)
            lines.append([src, tar])
        elif l.is_outgoing():
            src = fd.get_point(l.target)
            tar = Point(l.x, l.y)
            lines.append([src, tar])

    ci = 0
    for i, l1 in enumerate(lines):
        for j, l2 in enumerate(lines):
            # test if the lines cross, without changing the lines
            if i == j:
                continue
            if intersect(l1[0], l1[1], l2[0], l2[1]):
                ci += 1
    return ci


def auto_remove_intersections_by_align_legs(fd):
    fd = auto_align_legs(fd)
    min_intersections = _compute_number_of_intersects(fd)
    min_perm = 0
    inc = [l for l in fd.legs if l.is_incoming()]
    outc = [l for l in fd.legs if l.is_outgoing()]
    xyin = [[l.x, l.y] for l in inc]
    xyout = [[l.x, l.y] for l in outc]
    # loop over all permutations of incoming and outgoing legs
    for i, o in itertools.product(set(permutations(inc)), set(permutations(outc))):
        for xyi, l in zip(xyin, i):
            l.x = xyi[0]
            l.y = xyi[1]
        for xyo, l in zip(xyout, o):
            l.x = xyo[0]
            l.y = xyo[1]
        ci = _compute_number_of_intersects(fd)
        if ci < min_intersections:
            min_intersections = ci
            min_perm = (i, o)
            logging.debug(f"auto_remove_intersections_by_align_legs: {ci}")
            logging.debug(f"auto_remove_intersections_by_align_legs: {i} {o}")
            logging.debug(f"auto_remove_intersections_by_align_legs: {xyin} {xyout}")
    # use/return best permutation
    for xyi, l in zip(xyin, min_perm[0]):
        l.x = xyi[0]
        l.y = xyi[1]
    for xyo, l in zip(xyout, min_perm[1]):
        l.x = xyo[0]
        l.y = xyo[1]
    return fd


def auto_align_legs(fd, incoming=None, outgoing=None):
    """
    Automatically reshuffle the legs of a Feynman diagram.
    """
    f_min_x, f_min_y, f_max_x, f_max_y = fd.get_bounding_box()
    if incoming is None:
        incoming = [
            [f_min_x, y] for y in np.linspace(f_min_y, f_max_y, len(fd.incoming))
        ]
    if outgoing is None:
        outgoing = [
            [f_max_x, y] for y in np.linspace(f_min_y, f_max_y, len(fd.outgoing))
        ]
    _auto_align([l for l in fd.legs if l.is_incoming()], incoming)
    _auto_align([l for l in fd.legs if l.is_outgoing()], outgoing)
    return fd


def _auto_align(points, positions):
    """
    Automatically position the vertices and legs on a list of positions.
    """
    logging.debug(f"_auto_align: positions {positions}")
    # check if a vertex or leg is missing a x or y position
    require_xy(points)
    vpl = len(points)
    # table of distances between vertices v and points p
    dist = np.ones((vpl, len(positions))) * np.inf
    for i, v in enumerate():
        for j, p in enumerate(positions):
            dist[i][j] = np.sqrt((v.x - p[0]) ** 2 + (v.y - p[1]) ** 2)
    for i in range(vpl):
        min_i, min_j = np.unravel_index(dist.argmin(), dist.shape)
        v = points[min_i]
        v.x = positions[min_j][0]
        v.y = positions[min_j][1]
        # remove min_i and min_j from dist
        dist[min_i, :] = np.inf
        dist[:, min_j] = np.inf


def auto_align(fd, positions):
    """
    Automatically position the vertices and legs on a list of positions.

    Parameters
    ----------
    fd : FeynmanDiagram
        The Feynman diagram to be positioned.
    positions : list of tuple
        A list of tuples of the form (x,y) with the positions of the vertices

    Returns
    -------
    FeynmanDiagram
        The Feynman diagram with the vertices and legs positioned.
    """
    _auto_align([*fd.vertices, *fd.legs], positions)
    return fd


def auto_grid(fd, n_x=None, n_y=None, min_x=None, min_y=None, max_x=None, max_y=None):
    """
    Automatically position the vertices and legs on a grid, with the given
    minimum and maximum values for x and y, and the number of grid points, but
    avoid placing vertices or legs on the same position.
    """
    # get the bounding box and construct grid from that
    f_min_x, f_min_y, f_max_x, f_max_y = fd.get_bounding_box()
    if n_x is None:
        n_x = len(fd.vertices) + len(fd.legs)
    if n_y is None:
        n_y = len(fd.vertices) + len(fd.legs)
    if min_x is None:
        min_x = f_min_x
    if max_x is None:
        max_x = f_max_x
    if min_y is None:
        min_y = f_min_y
    if max_y is None:
        max_y = f_max_y
    logging.debug(f"auto_grid {n_x}, {n_y}, {min_x}, {min_y}, {max_x}, {max_y}")

    xvalues = np.linspace(min_x, max_x, n_x)
    yvalues = np.linspace(min_y, max_y, n_y)
    xx, yy = np.meshgrid(xvalues, yvalues)
    positions = [[x, y] for x, y in zip(xx.flatten(), yy.flatten())]
    return auto_align(fd, positions)


def auto_position(fd, layout="neato", clear_vertices=True):
    """Automatically position the vertices and legs."""
    # fd = scale_positions(fd, 10)
    fd = fd.with_style(f"layout : {layout}")
    fd = incoming_to_left(fd)
    fd = outgoing_to_right(fd)
    fd = feynman_adjust_points(fd, size=5, clear_vertices=clear_vertices)
    # fd = remove_unnecessary_vertices(fd)
    return fd


def incoming_to_left(fd):
    """Set the incoming legs to the left."""
    n = 0
    for l in fd.legs:
        if l.is_incoming():
            l.x = -2
            n = n + 1
    i = 0
    for l in fd.legs:
        if l.is_incoming():
            l.y = 4 / n * i
            i = i + 1

    return fd


def outgoing_to_right(fd):
    """Set the outgoing legs to the right."""
    n = 0
    for l in fd.legs:
        if not l.is_incoming():
            l.x = 2
            n = n + 1
    i = 0
    for l in fd.legs:
        if not l.is_incoming():
            l.y = 4 / n * i
            i = i + 1
    return fd


def scale_positions(fd, scale):
    """Scale the positions of the vertices and legs."""
    for v in fd.vertices:
        v.x *= scale
        v.y *= scale
    return fd


def feynman_adjust_points(feyndiag, size=5, clear_vertices=False):
    """Adjust the points of the vertices and legs using Dot language algorithms."""
    fd = feyndiag
    if clear_vertices:
        for v in fd.vertices:
            v.x = None
            v.y = None
    norm = size
    dot = feynman_to_dot(fd, resubstituteslash=False)
    positions = dot_to_positions(dot)
    mmax = 0
    for _, p in positions.items():
        if p[0] > mmax:
            mmax = p[0]
        if p[1] > mmax:
            mmax = p[1]
    for v in fd.vertices:
        if v.id in positions:
            v.x = positions[v.id][0] / mmax * norm
            v.y = positions[v.id][1] / mmax * norm
    for l in fd.legs:
        l.x = positions[l.id][0] / mmax * norm
        l.y = positions[l.id][1] / mmax * norm
    return fd


def remove_unnecessary_vertices(feyndiag):
    """Remove vertices that are only connected to two vertices with the same propagator."""
    fd = feyndiag
    vertices = []
    for v in fd.vertices:
        ps = fd.get_connections(v)
        if (
            len(ps) == 2
            and ps[0].pdgid == ps[1].pdgid
            and isinstance(ps[0], Propagator)
            and isinstance(ps[1], Propagator)
        ):
            if ps[0].source == v.id and ps[1].target == v.id:
                ps[0].source = ps[1].source
                fd.remove_propagator(ps[1])
            elif ps[0].target == v.id and ps[1].source == v.id:
                ps[1].source = ps[0].source
                fd.remove_propagator(ps[0])
            else:
                raise Exception(
                    f"Unknown case, source == source or target == target, {v} {ps[0]} {ps[1]}"
                )
            continue
        vertices.append(v)
    fd.vertices = vertices
    return fd
