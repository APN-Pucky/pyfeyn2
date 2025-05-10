import tempfile
from typing import List

from pylatex import Command
from pylatex.utils import NoEscape

from pyfeyn2.render.latex.latex import LatexRender
from pyfeyn2.render.render import Render
from pyfeyn2.render.root.pyfeyn import Propagator, Vertex
from pyfeyn2.render.root.rootrender import ROOTRender


def root_to_latex(root_canvas) -> str:
    # create a tmp tex file
    with tempfile.NamedTemporaryFile(
        suffix=".tex", delete=True, mode="w+"
    ) as temp_file:
        root_canvas.SaveAs(temp_file.name)
        # read the file
        tex_src = temp_file.read()
        return tex_src
    raise RuntimeError("Failed to create temporary file")


class ROOTPDFRender(LatexRender, ROOTRender):
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
        # self.preamble.append(Command("RequirePackage", "luatex85"))
        self.preamble.append(Command("usepackage", NoEscape("tikz")))
        self.preamble.append(Command("usetikzlibrary", NoEscape("patterns")))
        self.preamble.append(Command("usetikzlibrary", NoEscape("plotmarks")))
        # fhout.write("\\usetikzlibrary{patterns}\n")
        # fhout.write("\\usetikzlibrary{plotmarks}\n")

    def render(
        self,
        file=None,
        show=True,
        resolution=100,
        width=None,
        height=None,
        clean_up=True,
    ):
        # First need to convert feynman to ROOT through ROOTRender
        ROOTRender.render(
            self,
            file=None,
            show=False,
            resolution=resolution,
            width=width,
            height=height,
        )
        # Then convert ROOT to LaTeX
        self.set_src_diag(NoEscape(root_to_latex(self.get_src_root())))
        LatexRender.render(self, file, show, resolution, width, height, clean_up)

    @classmethod
    def valid_styles(cls) -> bool:
        return super().valid_styles() + [
            "line",
            "symbol",
            "symbol-size",
            "color",
            "opacity",
            "bend-direction",
            "bend-in",
            "bend-out",
            "bend-loop",
            "bend-min-distance",
            "momentum-arrow",
            "momentum-arrow-sense",
            "double-distance",
            "label-side",
        ]

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
        return super().valid_types() + []

    @classmethod
    def valid_shapes(cls) -> List[str]:
        return super().valid_types() + []
