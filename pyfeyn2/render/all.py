import importlib
import shutil
import tempfile
import traceback
from typing import List

from feynml.shape import get_shapes
from feynml.type import get_types
from matplotlib import pyplot as plt
from pylatex import Figure, NoEscape, SubFigure

from pyfeyn2.render.js.mermaid import MermaidRender
from pyfeyn2.render.latex.dot import DotRender
from pyfeyn2.render.latex.feynmp import FeynmpRender
from pyfeyn2.render.latex.latex import LatexRender
from pyfeyn2.render.latex.tikzfeynman import TikzFeynmanRender
from pyfeyn2.render.mpl.feynmanrender import FeynmanRender
from pyfeyn2.render.ps.madgraph import MadGraphRender
from pyfeyn2.render.pyx.pyxrender import PyxRender
from pyfeyn2.render.text.ascii import ASCIIRender
from pyfeyn2.render.text.asciipdf import ASCIIPDFRender
from pyfeyn2.render.text.unicode import UnicodeRender
from pyfeyn2.render.text.unicodepdf import UnicodePDFRender

renders = {
    "tikz": TikzFeynmanRender,
    "pyx": PyxRender,
    "feynmp": FeynmpRender,
    "feynman": FeynmanRender,
    "dot": DotRender,
    "mermaid": MermaidRender,
    "asciipdf": ASCIIPDFRender,
    "unicodepdf": UnicodePDFRender,
    "madgraph": MadGraphRender,
}


def class_for_name(module_name, class_name):
    # load the module, will raise ImportError if module cannot be loaded
    m = importlib.import_module(module_name)
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, class_name)
    return c


def renderer_from_string(s):
    if s is None:
        return None
    elif s.lower() == "ascii":
        return ASCIIRender
    elif s.lower() == "unicode":
        return UnicodeRender
    elif s.lower() in renders:
        return renders[s.lower()]
    else:
        return class_for_name(".".join(s.split(".")[0:-1]), s.split(".")[-1])


class AllRender(LatexRender):
    """Render all diagrams to PDF."""

    def __init__(
        self,
        fd=None,
        documentclass="standalone",
        document_options=None,
        *args,
        **kwargs,
    ):
        if document_options is None:
            document_options = ["varwidth"]
        super().__init__(
            *args,
            fd=fd,
            documentclass=documentclass,
            document_options=document_options,
            **kwargs,
        )

    def render(
        self,
        file=None,
        show=True,
        subfigure=False,
        resolution=None,
        width=None,
        height=None,
    ):
        fd = self.fd
        self.dirpath = tempfile.mkdtemp()
        dirpath = self.dirpath

        dynarg = {}
        if show and not subfigure:
            dynarg["show"] = True
            if resolution is not None:
                dynarg["resolution"] = resolution
            if width is not None:
                dynarg["width"] = width
            if height is not None:
                dynarg["height"] = height
        else:
            dynarg = {"show": False}

        with self.create(Figure(position="h!")):
            for i, name in enumerate(renders):
                render = renders[name]
                if name == "all":
                    continue
                try:
                    if not subfigure:
                        print(name + ":")
                    render(fd).render(dirpath + "/" + name + ".pdf", **dynarg)
                    plt.close()
                except Exception:
                    print(name + " failed:")
                    print(traceback.format_exc())
                with self.create(SubFigure(position="b")) as subfig:
                    subfig.add_image(
                        dirpath + "/" + name + ".pdf",
                        width=NoEscape("0.49\\textwidth"),
                    )
                    subfig.add_caption(name)
                if i % 2 == 1:
                    self.append(NoEscape(r"\\"))

        if subfigure:
            super().render(file, show, resolution, width, height)
        shutil.rmtree(self.dirpath)

    @classmethod
    def valid_styles(style: str) -> List[str]:
        return sorted(list({i for r in renders.values() for i in r.valid_styles()}))

    @classmethod
    def valid_attributes(attr: str) -> List[str]:
        return sorted(list({i for r in renders.values() for i in r.valid_attributes()}))

    @classmethod
    def valid_types(typ: str) -> List[str]:
        return sorted(get_types())
        # return [i for r in renders.values() for i in r.valid_types()]

    @classmethod
    def valid_shapes(typ: str) -> List[str]:
        return sorted(get_shapes())
