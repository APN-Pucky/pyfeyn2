import tempfile
from typing import List

import ROOT
from pylatex import Command
from pylatex.utils import NoEscape

from pyfeyn2.render.latex.latex import LatexRender
from pyfeyn2.render.render import Render
from pyfeyn2.render.root.pyfeyn import Label, Propagator, Vertex

type_map = {
    "line": "line",
    "photon": "wavyline",
    "gluon": "curlyline",
    "gluino": "curlystraightline",
    "charged boson": "wavystraightline",
    "higgs": "dashedline",
    "ghost": "dottedline",
}


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


def get_property(fd, obj, prop, default=None):
    style = fd.get_style(obj)
    if style.getProperty(prop) is not None:
        return style.getProperty(prop).value
    else:
        return default


def get_property_value(style, prop, default=None):
    if style.getProperty(prop) is not None:
        return style.getProperty(prop).value
    else:
        return default


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

        minx, miny, maxx, maxy = self.fd.get_bounding_box()
        marginx = (maxx - minx) * 0.05
        marginy = (maxy - miny) * 0.05
        canvas = ROOT.TCanvas("c", "A canvas", 10, 10, width, height)
        canvas.Range(minx - marginx, miny - marginy, maxx + marginx, maxy + marginy)

        vertex_to_vertex = {}

        for v in self.fd.vertices:
            ox = get_property(self.fd, v, "label-offset-x", 0)
            oy = get_property(self.fd, v, "label-offset-y", 0)
            vertex_to_vertex[v.id] = Vertex(
                v.x,
                v.y,
                label=Label(text=v.label, offsetx=ox, offsety=oy),
            )
        for l in self.fd.legs:
            # ox = get_property(self.fd, l, "label-offset-x", 0)
            # oy = get_property(self.fd, l, "label-offset-y", 0)
            vertex_to_vertex[l.id] = Vertex(
                l.x,
                l.y,
                # label=Label(text = l.label, offsetx=ox, offsety=oy),
            )

        for p in self.fd.propagators:
            style = self.fd.get_style(p)
            ox = get_property_value(style, "label-offset-x", 0)
            oy = get_property_value(style, "label-offset-y", 0)
            double_distance = int(get_property_value(style, "double-distance", "3"))
            Propagator(
                vertex_to_vertex[p.source],
                vertex_to_vertex[p.target],
                typ=get_property_value(style, "line", "line"),
                label=Label(text=p.label, offsetx=ox, offsety=oy),
                linecolor=style.color,
                double_distance=double_distance,
            ).draw()
        for l in self.fd.legs:
            style = self.fd.get_style(l)
            ox = get_property_value(style, "label-offset-x", 0)
            oy = get_property_value(style, "label-offset-y", 0)
            double_distance = int(get_property_value(style, "double-distance", "3"))
            if l.is_incoming():
                src, tgt = l.target, l.id
            else:
                src, tgt = l.id, l.target

            Propagator(
                vertex_to_vertex[src],
                vertex_to_vertex[tgt],
                typ=get_property_value(style, "line", "line"),
                label=Label(text=l.label, offsetx=ox, offsety=oy),
                linecolor=style.color,
                double_distance=double_distance,
            ).draw()

        if show:
            canvas.Update()
        self.set_src_root(canvas)
        return canvas

    @classmethod
    def valid_styles(cls) -> bool:
        return super().valid_styles() + [
            "line",
            "label-offset-x",
            "label-offset-y",
            "double-distance",
            "color",
            # "symbol",
            # "symbol-size",
            # "opacity",
            # "bend-direction",
            # "bend-in",
            # "bend-out",
            # "bend-loop",
            # "bend-min-distance",
            # "momentum-arrow",
            # "momentum-arrow-sense",
            # "label-side",
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
        return super().valid_types() + [
            "baryon",
            "anti baryon",
            "line",
            "photon",
            "gluon",
            "gluino",
            "charged boson",
            "higgs",
            "ghost",
            "phantom",
            "boson",
            "fermion",
            "anti fermion",
        ]

    @classmethod
    def valid_shapes(cls) -> List[str]:
        return super().valid_types() + []
