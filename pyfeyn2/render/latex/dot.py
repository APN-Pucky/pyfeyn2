from typing import List

from pylatex import Command
from pylatex.utils import NoEscape

from pyfeyn2.feynmandiagram import Connector, FeynmanDiagram
from pyfeyn2.interface.dot import (
    REPLACE_THIS_WITH_A_BACKSLASH,
    dot_to_tikz,
    feynman_to_dot,
)
from pyfeyn2.render.latex.latex import LatexRender

# workaround for dot2tex bug in math mode labels
# https://tikz.dev/tikz-decorations
map_feyn_to_tikz = {
    "vector": "decorate,decoration=snake",
    "boson": "decorate,decoration=snake",
    "photon": "decorate,decoration=snake",
    "gluon": "decorate,decoration={coil,aspect=0.3,segment length=1mm}",
    "ghost": "dotted",
    "fermion": "decorate,postaction={decorate,draw,red,decoration={markings,mark=at position 0.5 with {\\arrow{>}}}}",
    "anti fermion": "decorate,postaction={decorate,draw,red,decoration={markings,mark=at position 0.5 with {\\arrow{<}}}}",
    "higgs": "densely dashed",
    "scalar": "densely dashed",
    "slepton": "densely dashed",
    "squark": "densely dashed",
    "zigzag": "decorate,decoration=zigzag",
    "line": "draw",
    "phantom": "draw=none",
}


def stylize_connect(fd: FeynmanDiagram, c: Connector) -> str:
    fstyle = fd.get_style(c)
    if fstyle.getProperty("line") is not None:
        lname = fstyle.getProperty("line").value
    else:
        lname = c.type  # fallback to type if no style
    style = 'style="{}",texmode="raw"'.format(map_feyn_to_tikz[lname])
    if c.label is None:
        label = ""
    else:
        label = c.label.replace("\\", REPLACE_THIS_WITH_A_BACKSLASH)
    if fstyle.getProperty("length") is not None:
        leng = fstyle.getProperty("length").value
        style += f",len={leng}"
    style += f',label="{label}"'
    return style


class DotRender(LatexRender):
    def __init__(
        self,
        fd=None,
        documentclass="standalone",
        document_options=None,
        *args,
        **kwargs,
    ):
        if document_options is None:
            document_options = ["preview", "crop", "tikz"]
        super().__init__(
            *args,
            fd=fd,
            documentclass=documentclass,
            document_options=document_options,
            **kwargs,
        )
        # super(Render,self).__init__(*args, fd=fd,**kwargs)
        self.preamble.append(Command("usepackage", NoEscape("tikz")))
        self.preamble.append(
            Command("usetikzlibrary", NoEscape("snakes,arrows,shapes"))
        )
        self.preamble.append(Command("usepackage", NoEscape("amsmath")))
        self.preamble.append(
            Command("usetikzlibrary", NoEscape("decorations.markings"))
        )
        if fd is not None:
            self.set_feynman_diagram(fd)

    def set_feynman_diagram(self, fd):
        super().set_feynman_diagram(fd)
        self.src_dot = feynman_to_dot(
            fd, styler=stylize_connect, resubstituteslash=False
        )
        self.set_src_diag(dot_to_tikz(self.src_dot))
        self.src_dot = self.src_dot.replace(REPLACE_THIS_WITH_A_BACKSLASH, "\\")

    def get_src_dot(self):
        return self.src_dot

    @classmethod
    def valid_attributes(cls) -> List[str]:
        return super().valid_attributes() + [
            "x",
            "y",
            "label",
            "style",
        ]

    @classmethod
    def valid_types(cls) -> List[str]:
        return super().valid_types() + list(map_feyn_to_tikz.keys())

    @classmethod
    def valid_styles(cls) -> bool:
        return super().valid_styles() + [
            "line",
            "direction",
            "layout",
            "length",
        ]
