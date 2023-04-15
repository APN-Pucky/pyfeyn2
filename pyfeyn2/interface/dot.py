from warnings import warn

import dot2tex

REPLACE_THIS_WITH_A_BACKSLASH = "¬"


def _fake_styler(fd, p):
    return 'style="draw=none"'


def get_rankdir(fdstyle):
    rankdir = None
    if fdstyle.getProperty("direction") is None:
        warn("direction is unkown, using default of 'right'")
        rankdir = "LR"
    else:
        rdir = fdstyle.getProperty("direction").value
        if rdir == "right":
            rankdir = "LR"
        elif rdir == "left":
            rankdir = "RL"
        elif rdir == "down":
            rankdir = "TB"
        elif rdir == "up":
            rankdir = "BT"
        else:
            raise Exception(f"Unknown direction: {rdir}")
    return rankdir


def get_layout(fdstyle):
    layout = None
    if fdstyle.getProperty("layout") is None:
        warn("layout is unknwon, using default of 'dot'")
        layout = "dot"
    else:
        layout = fdstyle.getProperty("layout").value
    return layout


def feynman_to_dot(fd, resubstituteslash=True, styler=_fake_styler):
    # TODO better use pydot? still alive? or grpahviz?
    fdstyle = fd.get_style(fd)
    rankdir = get_rankdir(fdstyle)
    layout = get_layout(fdstyle)

    thestyle = ""
    src = "graph G {\n"
    src += f"rankdir={rankdir};\n"
    src += f"layout={layout};\n"
    # src += "mode=hier;\n"
    src += 'node [style="invis"];\n'
    # nodes
    for l in fd.legs + fd.vertices:
        if l.x is not None and l.y is not None:
            src += f'\t\t{l.id} [ pos="{l.x},{l.y}!"];\n'
    # edges
    for p in fd.propagators:
        if styler is not None:
            thestyle = styler(fd, p)
        src += f"edge [{thestyle}];\n"
        src += f"\t\t{p.source} -- {p.target};\n"
    rank_in = "{rank=min; "
    rank_out = "{rank=max; "

    # edges
    for l in fd.legs:
        if styler is not None:
            thestyle = styler(fd, l)
        if l.sense == "incoming":
            src += f"edge [{thestyle}];\n"
            src += f"\t\t{l.id} -- {l.target};\n"
            rank_in += f"{l.id} "
        elif l.sense == "outgoing":
            src += f"edge [{thestyle}];\n"
            src += f"\t\t{l.target} -- {l.id};\n"
            rank_out += f"{l.id} ;"
        else:
            # TODO maybe not error but just use the default
            raise Exception("Unknown sense")
    src += rank_in + "}\n"
    src += rank_out + "}\n"
    src += "}"
    if resubstituteslash:
        src = src.replace(REPLACE_THIS_WITH_A_BACKSLASH, "\\")
    return src


def dot_to_positions(dot):
    ret = dot2tex.dot2tex(dot, format="positions")
    return ret


def dot_to_tikz(dot):
    ret = dot2tex.dot2tex(dot, format="tikz", figonly=True)
    ret = ret.replace(REPLACE_THIS_WITH_A_BACKSLASH, "\\")
    return ret
