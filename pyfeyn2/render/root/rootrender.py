import tempfile
from typing import List

from pylatex import Command
from pylatex.utils import NoEscape

from pyfeyn2.render.latex.latex import LatexRender
from pyfeyn2.render.render import Render
from pyfeyn2.render.root.pyfeyn import Propagator, Vertex


def root_to_cpp(root_canvas) -> str:
    # create a tmp tex file
    with tempfile.NamedTemporaryFile(
        suffix=".tex", delete=True, mode="w+"
    ) as temp_file:
        root_canvas.SaveSource(temp_file.name)
        # read the file
        tex_src = temp_file.read()
        return tex_src
    raise RuntimeError("Failed to create temporary file")


class ROOTRender(Render):
    def __init__(self, fd=None, *args, **kwargs):
        super().__init__(fd, *args, **kwargs)

    def get_src_root(self):
        return self.src_root

    def set_src_root(self, src_root):
        self.src_root = src_root
        self.src_cpp = root_to_cpp(src_root)

    def render(
        self,
        file=None,
        show=True,
        resolution=100,
        width=None,
        height=None,
        clean_up=True,
    ):
        if width is None:
            width = 600
        if height is None:
            height = 600
        import ROOT

        minx, miny, maxx, maxy = self.fd.get_bounding_box()
        canvas = ROOT.TCanvas("c", "A canvas", 10, 10, width, height)
        canvas.Range(minx, miny, maxx, maxy)

        vertex_to_vertex = {}

        for v in self.fd.vertices:
            vertex_to_vertex[v.id] = Vertex(
                v.x,
                v.y,
            )
        for l in self.fd.legs:
            vertex_to_vertex[l.id] = Vertex(
                l.x,
                l.y,
            )

        for p in self.fd.propagators:
            Propagator(vertex_to_vertex[p.source], vertex_to_vertex[p.target]).draw()
        for l in self.fd.legs:
            if l.is_incoming():
                Propagator(vertex_to_vertex[l.id], vertex_to_vertex[l.target]).draw()
            else:
                Propagator(vertex_to_vertex[l.target], vertex_to_vertex[l.id]).draw()

        if show:
            canvas.Update()
        self.set_src_root(canvas)
        return canvas

    @classmethod
    def valid_styles(cls) -> bool:
        return super().valid_styles() + [
            "line",
            # "symbol",
            # "symbol-size",
            # "color",
            # "opacity",
            # "bend-direction",
            # "bend-in",
            # "bend-out",
            # "bend-loop",
            # "bend-min-distance",
            # "momentum-arrow",
            # "momentum-arrow-sense",
            # "double-distance",
            # "label-side",
        ]

    @classmethod
    def valid_attributes(cls) -> List[str]:
        return super().valid_attributes() + [
            "x",
            "y",
            # "label",
            # "style",
        ]

    @classmethod
    def valid_types(cls) -> List[str]:
        return super().valid_types() + []

    @classmethod
    def valid_shapes(cls) -> List[str]:
        return super().valid_types() + []
