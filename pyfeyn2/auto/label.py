import copy
from ast import List
from enum import Enum

from pylatexenc.latex2text import LatexNodes2Text


class LabelType(Enum):
    LATEX = 1
    UNICODE = 2
    ASCII = 3


def auto_label(
    objs: List, replace: bool = False, label_type: LabelType = LabelType.LATEX
):
    """
    Automatically label objects.

    Parameters
    ----------
    objs : list
        List of objects to label.
    replace : bool, optional
        Whether to replace existing labels. The default is False.

    """
    for p in objs:
        if (p.label is None or replace) and p.particle is not None:
            if label_type == LabelType.LATEX:
                p.label = "$" + p.particle.latex_name + "$"
            elif label_type == LabelType.UNICODE:
                p.label = LatexNodes2Text().latex_to_text(
                    "$" + p.particle.latex_name + "$"
                )
            elif label_type == LabelType.ASCII:
                p.label = p.particle.name
            else:
                raise Exception("Unknown label type.")


def auto_label_propagators(ifd, replace=False):
    """Automatically label propagators."""
    # fd = copy.deepcopy(ifd)
    fd = ifd
    objs = fd.propagators
    for p in objs:
        if p.label is None or replace:
            p.label = "$" + p.particle.latex_name + "$"
    return fd


def auto_label_legs(ifd, replace=False):
    """Automatically label legs."""
    # fd = copy.deepcopy(ifd)
    fd = ifd
    objs = fd.legs
    for p in objs:
        if p.particle is None or replace:
            p.particle = "$" + p.particle.latex_name + "$"
    return fd
