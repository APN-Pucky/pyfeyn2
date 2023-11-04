import base64
from typing import List

import requests
from IPython.display import Image, display

from pyfeyn2.render.render import Render


def mm(graph):
    graphbytes = graph.encode("utf8")
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    r = requests.get("https://mermaid.ink/svg/" + base64_string)
    return r.content

    display(Image(url="" + base64_string))


def feynman_to_mm(fd):
    src = "graph LR;\n"
    for v in fd.vertices:
        src += f"{v.id}(vertex);\n"
    for l in fd.legs:
        src += f"{l.id}(leg);\n"
    for l in fd.legs:
        src += f"{l.id} --> {l.target};\n"
    for p in fd.propagators:
        src += f"{p.source} --> {p.target};\n"
    return src


class MermaidRender(Render):
    def __init__(
        self,
        fd=None,
        *args,
        **kwargs,
    ):
        super().__init__(self, fd)

    def render(
        self,
        file=None,
        show=True,
    ):
        svg = mm(self.get_src())
        if file:
            with open(file + ".svg", "wb") as f:
                f.write(svg)
        img = Image(data=svg)
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
        return super().valid_types() + list(type_map.keys())

    @classmethod
    def valid_shapes(cls) -> List[str]:
        return super().valid_types() + list(shape_map.keys())
