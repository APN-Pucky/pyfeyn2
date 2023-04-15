import uuid
from typing import List

from pylatex import Command
from pylatex.utils import NoEscape

from pyfeyn2 import feynmandiagram
from pyfeyn2.feynmandiagram import Connector
from pyfeyn2.render.latex.metapost import MetaPostRender

# converte FeynmanDiagram to tikz-feynman

type_map = {
    "line": ["plain"],
    "gluon": ["gluon"],
    "curly": ["curly"],
    "dbl_curly": ["dbl_curly"],
    "dashes": ["dashes"],
    "scalar": ["scalar"],
    "dashes_arrow": ["dashes_arrow"],
    "dbl_dashes": ["dbl_dashes"],
    "dbl_dashes_arrow": ["dbl_dashes_arrow"],
    "dots": ["dots"],
    "dots_arrow": ["dots_arrow"],
    "ghost": ["ghost"],
    "dbl_dots": ["dbl_dots"],
    "dbl_dots_arrow": ["dbl_dots_arrow"],
    "phantom": ["phantom"],
    "phantom_arrow": ["phantom_arrow"],
    "plain": ["plain"],
    "plain_arrow": ["plain_arrkddow"],
    "fermion": ["fermion"],
    "anti fermion": ["fermion"],
    "electron": ["electron"],
    "quark": ["quark"],
    "double": ["double"],
    "dbl_plain": ["dbl_plain"],
    "double_arrow": ["double_arrow"],
    "dbl_plain_arrow": ["dbl_plain_arrow"],
    "heavy": ["heavy"],
    "photon": ["photon"],
    "boson": ["boson"],
    "wiggly": ["wiggly"],
    "dbl_wiggly": ["dbl_wiggly"],
    "zigzag": ["zigzag"],
    "dbl_zigzag": ["dbl_zigzag"],
    "higgs": ["dashes"],
    "vector": ["boson"],
    "slepton": ["scalar"],
    "squark": ["scalar"],
    "gluino": ["gluon", "plain"],
    "gaugino": ["photon", "plain"],
}


def stylize_line(fd: feynmandiagram, c: Connector) -> str:
    cstyle = fd.get_style(c)
    style = ""
    if c.label is not None:
        style += f",label={c.label}"
    if cstyle.getProperty("tension") is not None:
        style += ",tension=" + str(cstyle.getProperty("tension").value)
    return style


def feynman_to_feynmp(fd):
    dire = fd.get_style(fd).getProperty("direction").value
    dirin = ""
    dirout = ""
    if dire == "left":
        dirin = "right"
        dirout = "left"
    elif dire == "right":
        dirin = "left"
        dirout = "right"
    elif dire == "up":
        dirin = "bottom"
        dirout = "top"
    elif dire == "down":
        dirin = "top"
        dirout = "bottom"
    else:
        raise Exception(f"Unknown direction: {dire}")

    # get random alphanumeric string
    result_str = uuid.uuid4().hex
    src = "\\begin{fmffile}{tmp-" + result_str + "}\n"
    src += "\\begin{fmfgraph*}(120,80)\n"
    incoming = []
    outgoing = []
    # Collect incoming and outgoing legs
    for l in fd.legs:
        if l.sense == "incoming":
            incoming += [l]
        elif l.sense == "outgoing":
            outgoing += [l]
        else:
            raise Exception("Unknown sense")
    if len(incoming) > 0:
        src += f"\t\t\\fmf{dirin}" + "{"
        for l in incoming:
            src += f"{l.id},"
        src = src[:-1]
        src += "}\n"
    if len(outgoing) > 0:
        src += f"\t\t\\fmf{dirout}" + "{"
        for l in outgoing:
            src += f"{l.id},"
        src = src[:-1]
        src += "}\n"

    def do_legs(src, legs, inward):
        for l in legs:
            lstyle = fd.get_style(l)
            if lstyle.getProperty("line") is not None:
                tttype = type_map[lstyle.getProperty("line").value]
            else:
                tttype = l.type  # fallback to type if no line style is set
            style = stylize_line(fd, l)
            for ttype in tttype:
                lid = l.id
                ltarget = l.target
                if l.type.startswith("anti"):
                    lid = l.target
                    ltarget = l.id
                if inward:
                    src += f"\t\t\\fmf{{{ttype}{style}}}{{{lid},{ltarget}}}\n"
                else:
                    src += f"\t\t\\fmf{{{ttype}{style}}}{{{ltarget},{lid}}}\n"
                style = ""
        return src

    src = do_legs(src, incoming, True)
    src = do_legs(src, outgoing, False)

    for p in fd.propagators:
        pstyle = fd.get_style(p)
        if pstyle.getProperty("line") is not None:
            tttype = type_map[pstyle.getProperty("line").value]
        else:
            tttype = p.type  # fallback to type if no line style is set
        style = stylize_line(fd, p)
        for ttype in tttype:
            psource = p.source
            ptarget = p.target
            if p.type.startswith("anti"):
                psource = p.target
                ptarget = p.source
            src += f"\t\t\\fmf{{{ttype}{style}}}{{{psource},{ptarget}}}\n"
            style = ""

    # Add labels
    for v in fd.vertices:
        if v.label is not None:
            src += f"\t\t\\fmflabel{{{v.label}}}{{{v.id}}}\n"
    src += "\\end{fmfgraph*}\n"
    src += "\\end{fmffile}\n"
    return src


class FeynmpRender(MetaPostRender):
    def __init__(
        self,
        fd=None,
        documentclass="standalone",
        document_options=None,
        *args,
        **kwargs,
    ):
        if document_options is None:
            document_options = ["preview", "crop"]
        super().__init__(
            *args,
            fd=fd,
            documentclass=documentclass,
            document_options=document_options,
            **kwargs,
        )
        self.preamble.append(Command("usepackage", NoEscape("feynmp-auto")))
        if fd is not None:
            self.set_feynman_diagram(fd)

    def set_feynman_diagram(self, fd):
        super().set_feynman_diagram(fd)
        self.set_src_diag(NoEscape(feynman_to_feynmp(fd)))

    @classmethod
    def valid_attributes(cls) -> List[str]:
        return super(FeynmpRender, cls).valid_attributes() + ["label", "style"]

    @classmethod
    def valid_types(cls) -> List[str]:
        return super(FeynmpRender, cls).valid_types() + list(type_map.keys())

    @classmethod
    def valid_styles(cls) -> bool:
        return super(FeynmpRender, cls).valid_styles() + [
            "line",
            "direction",
            "tension",
        ]
