import copy

import dot2tex
from pyfeyn2.interface.dot import (
    REPLACE_THIS_WITH_A_BACKSLASH,
    dot_to_tikz,
    feynman_to_dot,
)
from pylatex import Command
from pylatex.utils import NoEscape

from pyfeyn2.feynmandiagram import Connector
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
    "higgs": "densely dashed",
    "scalar": "densely dashed",
    "slepton": "densely dashed",
    "squark": "densely dashed",
    "zigzag": "decorate,decoration=zigzag",
    "phantom": "draw=none",
}


def stylize_connect(c: Connector) -> str:
    style = 'style="{}",texmode="raw"'.format(map_feyn_to_tikz[c.type])
    if c.label is None:
        label = ""
    else:
        label = c.label.replace("\\", REPLACE_THIS_WITH_A_BACKSLASH)
    if c.length is not None:
        style += f",len={c.length}"
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

    @staticmethod
    def valid_attribute(attr: str) -> bool:
        return super(DotRender, DotRender).valid_attribute(attr) or attr in [
            "x",
            "y",
            "label",
        ]

    @staticmethod
    def valid_type(typ):
        if typ.lower() in map_feyn_to_tikz:
            return True
        return False
