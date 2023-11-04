import base64
from typing import List

import requests
from IPython.display import SVG, display

from pyfeyn2.feynmandiagram import Connector, FeynmanDiagram
from pyfeyn2.render.render import Render


def mm(graph):
    graphbytes = graph.encode("utf8")
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    # print("graph: ", graph)
    # print("b64: ", base64_string)
    r = requests.get("https://mermaid.ink/svg/" + base64_string)
    return r.content


def stylize_connect(fd: FeynmanDiagram, c: Connector):
    ret = ""
    if c.label is None:
        ret = "---"
    else:
        ret = f"-- {c.label} ---"
    return ret


def feynman_to_mm(fd):
    src = "graph LR;\n"
    for v in fd.vertices:
        src += f"{v.id}:::hidden;\n"
    for l in fd.legs:
        src += f"{l.id}:::hidden;\n"
    for l in fd.legs:
        sty = stylize_connect(fd, l)
        if l.is_incoming():
            src += f"{l.id} {sty} {l.target};\n"
        elif l.is_outgoing():
            src += f"{l.target} {sty} {l.id};\n"
        else:
            raise Exception("Unknown leg sense. Should be either incoming or outgoing.")
    for p in fd.propagators:
        sty = stylize_connect(fd, p)
        src += f"{p.source} {sty} {p.target};\n"

    src += "classDef hidden display: none;\n"
    # print(src)
    return src


class MermaidRender(Render):
    def __init__(
        self,
        fd=None,
        *args,
        **kwargs,
    ):
        super().__init__(fd)
        self.set_feynman_diagram(fd)

    def render(
        self,
        file=None,
        show=True,
        resolution=100,
        width=None,
        height=None,
        clean_up=True,
    ):
        svg = mm(self.get_src())
        if file:
            with open(file + ".svg", "wb") as f:
                f.write(svg)
        img = SVG(data=svg)
        if show:
            display(img)
        return img

    def set_feynman_diagram(self, fd):
        super().set_feynman_diagram(fd)
        self.set_src(feynman_to_mm(fd))

    @classmethod
    def valid_styles(cls) -> bool:
        return super().valid_styles() + []

    @classmethod
    def valid_attributes(cls) -> List[str]:
        return super().valid_attributes() + [
            "label",
            "style",
        ]

    @classmethod
    def valid_types(cls) -> List[str]:
        return super().valid_types()

    @classmethod
    def valid_shapes(cls) -> List[str]:
        return super().valid_types()
