import numpy as np

from pyfeyn2.auto.bend import auto_bend
from pyfeyn2.auto.debug import auto_debug
from pyfeyn2.auto.label import auto_label
from pyfeyn2.auto.position import auto_align_legs, auto_vdw


def auto_default(
    fd,
    auto_position=True,
    auto_position_legs=True,
    debug=False,
):
    if auto_position:
        # remove all unpositioned vertices
        if auto_position_legs:
            fd = auto_align_legs(
                fd,
                incoming=[(0, i) for i in np.linspace(0, 10, len(fd.get_incoming()))],
                outgoing=[(10, i) for i in np.linspace(0, 10, len(fd.get_outgoing()))],
            )
        p = [v for v in fd.vertices if v.x is None or v.y is None]
        if len(p) > 0:
            fd = auto_vdw(fd, points=p)
        # if auto_position_legs:
        #    auto_remove_intersections_by_permuting_legs(fd, adjust_points=True)
        #    if len(p) > 0:
        #        fd = auto_vdw(fd, points=p)
    auto_label([*fd.propagators, *fd.legs])
    fd = auto_bend(fd)
    # Last step enable debug
    if debug:
        auto_debug(fd)
    return fd
