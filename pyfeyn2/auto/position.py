import itertools
import logging
from itertools import permutations

import iminuit
import numpy as np
from feynml import Leg, Point, Propagator

from pyfeyn2.interface.dot import dot_to_positions, feynman_to_dot


# from https://stackoverflow.com/a/9997374
def ccw(A, B, C):
    """
    Return true if the points A, B, and C are in counter-clockwise order.
    """
    return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)


# Return true if line segments AB and CD intersect
def intersect(A, B, C, D):
    """
    Return true if line segments AB and CD intersect

    Parameters
    ----------
    A : Point
        The first point of the first line segment.
    B : Point
        The second point of the first line segment.
    C : Point
        The first point of the second line segment.
    D : Point
        The second point of the second line segment.

    Returns
    -------
    bool
        True if the line segments intersect, False otherwise.

    Examples
    --------
    >>> A = Point(0, 0)
    >>> B = Point(1, 1)
    >>> C = Point(0, 1)
    >>> D = Point(1, 0)
    >>> intersect(A, B, C, D)
    True
    >>> A,B,C,D = Point(0,0), Point(1,1), Point(0,0), Point(1,0)
    >>> intersect(A, B, C, D)
    False
    """
    if A.x == C.x and A.y == C.y:
        return False
    if A.x == D.x and A.y == D.y:
        return False
    if B.x == C.x and B.y == C.y:
        return False
    if B.x == D.x and B.y == D.y:
        return False
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


def set_none_xy_to_zero(points):
    for p in points:
        if p.x is None:
            p.x = 0
        if p.y is None:
            p.y = 0


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
    points = [*fd.vertices, *fd.legs]
    require_xy(points)
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
        for _, l2 in enumerate(lines[i + 1 :]):
            # test if the lines cross, without changing the lines
            if intersect(l1[0], l1[1], l2[0], l2[1]):
                ci += 1
    return ci


def auto_remove_intersections_by_align_legs(fd, adjust_points=False, size=5):
    """
    Automatically remove intersections by aligning the legs and reshufffling (permuting) them.
    """
    fd = auto_align_legs(fd)
    if adjust_points:
        fd = feynman_adjust_points(fd, size=size, clear_vertices=True)
    min_intersections = np.inf
    min_perm = 0
    inc = [l for l in fd.legs if l.is_incoming()]
    outc = [l for l in fd.legs if l.is_outgoing()]
    xyin = [[l.x, l.y] for l in inc]
    xyout = [[l.x, l.y] for l in outc]
    # loop over all permutations of incoming and outgoing legs
    for i, o in itertools.product(
        set(permutations(range(len(inc)))), set(permutations(range(len(outc))))
    ):
        for xyi, l in zip(xyin, i):
            inc[l].x = xyi[0]
            inc[l].y = xyi[1]
        for xyo, l in zip(xyout, o):
            outc[l].x = xyo[0]
            outc[l].y = xyo[1]
        if adjust_points:
            fd = feynman_adjust_points(fd, size=size, clear_vertices=True)
        ci = _compute_number_of_intersects(fd)
        print(ci)
        logging.debug(f"auto_remove_intersections_by_align_legs: {ci}")
        if ci < min_intersections:
            min_intersections = ci
            min_perm = (i, o)
            logging.debug(f"auto_remove_intersections_by_align_legs: {ci}")
            logging.debug(f"auto_remove_intersections_by_align_legs: {i} {o}")
            logging.debug(f"auto_remove_intersections_by_align_legs: {xyin} {xyout}")
    # use/return best permutation
    for xyi, l in zip(xyin, min_perm[0]):
        inc[l].x = xyi[0]
        inc[l].y = xyi[1]
    for xyo, l in zip(xyout, min_perm[1]):
        outc[l].x = xyo[0]
        outc[l].y = xyo[1]
    if adjust_points:
        fd = feynman_adjust_points(fd, size=size, clear_vertices=True)
    return fd


def auto_align_legs(fd, incoming=None, outgoing=None):
    """
    Automatically reshuffle the legs of a Feynman diagram.
    """
    set_none_xy_to_zero(fd.legs)
    inc = [l for l in fd.legs if l.is_incoming()]
    outc = [l for l in fd.legs if l.is_outgoing()]
    if incoming is None or outgoing is None:
        f_min_x, f_min_y, f_max_x, f_max_y = fd.get_bounding_box()
        if incoming is None:
            incoming = [[f_min_x, y] for y in np.linspace(f_min_y, f_max_y, len(inc))]
        if outgoing is None:
            outgoing = [[f_max_x, y] for y in np.linspace(f_min_y, f_max_y, len(outc))]
    _auto_align(inc, incoming)
    _auto_align(outc, outgoing)
    return fd


def _get_dist(points, positions):
    dist = np.ones((len(points), len(positions))) * np.inf
    for i, v in enumerate(points):
        for j, p in enumerate(positions):
            dist[i][j] = np.sqrt((v.x - p[0]) ** 2 + (v.y - p[1]) ** 2)
    return dist


def _auto_align(points, positions):
    """
    Automatically position the vertices and legs on a list of positions.
    """
    logging.debug(f"_auto_align: positions {positions}")
    # check if a vertex or leg is missing a x or y position
    require_xy(points)
    # table of distances between vertices v and points p
    dist = _get_dist(points, positions)
    for i in range(len(points)):
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
    positions = _get_grid(fd, n_x, n_y, min_x, min_y, max_x, max_y)
    return auto_align(fd, positions)


def _get_grid(fd, n_x=None, n_y=None, min_x=None, min_y=None, max_x=None, max_y=None):
    logging.debug(f"_get_grid {n_x}, {n_y}, {min_x}, {min_y}, {max_x}, {max_y}")
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
    # print(min_x, max_x, min_y, max_y, n_x, n_y)
    xvalues = np.linspace(min_x, max_x, n_x)
    yvalues = np.linspace(min_y, max_y, n_y)
    xx, yy = np.meshgrid(xvalues, yvalues)
    positions = [[x, y] for x, y in zip(xx.flatten(), yy.flatten())]
    return positions


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
        if v.x is not None:
            v.x *= scale
        if v.y is not None:
            v.y *= scale
    for l in fd.legs:
        if l.x is not None:
            l.x *= scale
        if l.y is not None:
            l.y *= scale
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


def auto_vdw(fd, points=None, LJ=1.0, y_symmetry=0.0, x_symmetry=0.0, intersection=0.0):
    """
    Minimizes Lennard-Jones potential between vertices and legs (scaled by LJ).
    Further the function to be minimized gets punished by the number of intersections scaled by intersection.
    The function to be minimized gets punished by the asymmetry in x and y direction scaled by x_symmetry and y_symmetry.

    Parameters
    ----------
    fd : FeynmanDiagram
        The Feynman diagram to be positioned.
    points : list of Point, optional
        The points (leg or vertex) to be positioned. Recommended values are fd.vertices or [*fd.vertices, *fd.legs]
    LJ : float, optional
        The strength of the Lennard-Jones potential, by default 1.0
    y_symmetry : float, optional
        The strength of the punishment for asymmetry in y direction, by default 0.0
    x_symmetry : float, optional
        The strength of the punishment for asymmetry in x direction, by default 0.0
    intersection : float, optional
        The strength of the punishment for intersections, by default 0.0

    Returns
    -------
    FeynmanDiagram
        The Feynman diagram with the vertices and legs positioned.



    """
    if points is None:
        points = fd.vertices
    r = LJ
    all_points = [*fd.vertices, *fd.legs]
    set_none_xy_to_zero(points)
    # get distance to connected points
    cons = []
    # dist = []
    for p in points:
        n = []
        # dd = []
        for c in fd.get_neighbours(p):
            for j, pp in enumerate(all_points):
                if pp.x is None or pp.y is None:
                    continue
                if pp.id == c.id:
                    n.append(j)
                    # dd.append(np.sqrt((p.x - pp.x) ** 2 + (p.y - pp.y) ** 2))
        cons.append(n)
        # dist.append(dd)

    def fun(*args):
        for i, p in enumerate(points):
            p.x = args[2 * i]
            p.y = args[2 * i + 1]
        LenJ = 0
        if LJ != 0.0:
            for i, p in enumerate(points):
                for j in cons[i]:
                    if all_points[j].x is not None and all_points[j].y is not None:
                        LenJ = (
                            LenJ
                            - (
                                (
                                    (
                                        (
                                            (p.x - all_points[j].x) ** 2
                                            + (p.y - all_points[j].y) ** 2
                                        )
                                        ** 0.5
                                    )
                                    / r
                                )
                                ** 6
                            )
                            + (
                                (
                                    (
                                        (p.x - all_points[j].x) ** 2
                                        + (p.y - all_points[j].y) ** 2
                                    )
                                    ** 0.5
                                )
                                / r
                            )
                            ** 12
                        )
        inter = 0
        if intersection != 0.0:
            inter += intersection * _compute_number_of_intersects(fd)
        pun_x = 0
        if x_symmetry != 0.0:
            min_x, min_y, max_x, max_y = fd.get_bounding_box()
            # get averate x and y
            avg_x = (min_x + max_x) / 2
            avg_y = (min_y + max_y) / 2
            pun = 0
            for p in points:
                nx = p.x - 2 * (p.x - avg_x)
                # find nearest point to (nx, p.y)
                min_dist = np.inf
                for pp in all_points:
                    if pp.id == p.id or pp.x is None or pp.y is None:
                        continue
                    dist = np.sqrt((nx - pp.x) ** 2 + (p.y - pp.y) ** 2)
                    if dist < min_dist:
                        min_dist = dist
                pun += min_dist
            pun_x = pun
        pun_y = 0
        if y_symmetry != 0.0:
            min_x, min_y, max_x, max_y = fd.get_bounding_box()
            # get averate x and y
            avg_x = (min_x + max_x) / 2
            avg_y = (min_y + max_y) / 2
            pun = 0
            for p in points:
                ny = p.y - 2 * (p.y - avg_y)
                # find nearest point to (p.x, ny)
                min_dist = np.inf
                for pp in all_points:
                    if pp.id == p.id or pp.x is None or pp.y is None:
                        continue
                    dist = np.sqrt((p.x - pp.x) ** 2 + (ny - pp.y) ** 2)
                    if dist < min_dist:
                        min_dist = dist
                pun += min_dist
            pun_y = pun
        # TODO add punishment for intersections
        # TODO add punishment for asymmetry
        return LenJ + inter + pun_x * x_symmetry + pun_y * y_symmetry

    m = iminuit.Minuit(fun, *[0 for _ in range(len(points) * 2)])
    v = m.migrad()
    args = list(v.values.to_dict().values())
    for i, p in enumerate(points):
        p.x = args[2 * i]
        p.y = args[2 * i + 1]
    return fd


def auto_gridded_springs(
    fd,
    points=None,
    n_x=None,
    n_y=None,
    min_x=None,
    min_y=None,
    max_x=None,
    max_y=None,
    **kwargs,
):  # TODO replace kwargs by actual arguments (i.e. for documentation)
    fd = auto_vdw(fd, points, **kwargs)
    fd = auto_grid(
        fd, n_x=n_x, n_y=n_y, min_x=min_x, min_y=min_y, max_x=max_x, max_y=max_y
    )
    return fd
