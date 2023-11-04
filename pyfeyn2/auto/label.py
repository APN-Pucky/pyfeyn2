import copy


def auto_label(objs, replace=False, latex=True):
    """Automatically label objects."""
    for p in objs:
        if (p.label is None or replace) and p.particle is not None:
            if latex:
                p.label = "$" + p.particle.latex_name + "$"
            else:
                p.label = p.particle.name


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
