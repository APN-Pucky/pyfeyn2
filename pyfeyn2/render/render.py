import abc
from typing import List

from feynml.feynmandiagram import FeynmanDiagram
from feynml.leg import Leg
from feynml.propagator import Propagator
from feynml.vertex import Vertex


class Render:
    def __init__(self, fd=None):
        self.fd = fd
        self.src = ""

    def set_feynman_diagram(self, fd):
        self.fd = fd

    def get_src(self):
        return self.src

    def set_src(self, src):
        self.src = src

    @abc.abstractmethod
    def render(
        self,
        file=None,
        show=True,
        resolution=100,
        width=None,
        height=None,
        clean_up=True,
    ):
        """
        Render the diagram.
        """
        return

    @classmethod
    def valid_styles(cls) -> List[str]:
        return []

    @classmethod
    def valid_types(cls) -> List[str]:
        return []

    @classmethod
    def valid_shapes(cls) -> List[str]:
        return []

    @classmethod
    def valid_attributes(cls) -> List[str]:
        return ["type", "shape", "class"]

    @classmethod
    def valid_type(cls, typ: str) -> bool:
        return typ in cls.valid_types()

    @classmethod
    def valid_shape(cls, typ: str) -> bool:
        return typ in cls.valid_shapes()

    @classmethod
    def valid_style(cls, style: str) -> bool:
        return style in cls.valid_styles()

    @classmethod
    def valid_attribute(cls, attr: str) -> bool:
        return attr in cls.valid_attributes()

    def demo_propagator(self, propagator, show=True, label=None, shape=None, **kwargs):
        v1 = Vertex().with_xy(-2, -2)
        v2 = Vertex().with_xy(2, -2)
        if shape is not None:
            v1 = v1.with_shape(shape)
            v1 = v2.with_shape(shape)

        fd = FeynmanDiagram().add(
            v1,
            v2,
            Propagator()
            .connect(v1, v2)
            .with_type(propagator)
            .with_label(label if label else propagator)
            .with_tension(0.0),
            Leg()
            .with_target(v1)
            .with_point(v1)
            .with_type("phantom")
            .with_incoming()
            .with_length(0.0),
            Leg()
            .with_target(v2)
            .with_point(v2)
            .with_type("phantom")
            .with_outgoing()
            .with_length(0.0),
        )

        self.set_feynman_diagram(fd)
        self.render(show=show, **kwargs)

    def demo_vertex(self, vertex, show=True, label=None):
        v1 = (
            Vertex()
            .with_xy(0, 0)
            .with_shape(vertex)
            .with_label(label if label else vertex)
        )

        fd = FeynmanDiagram().add(
            v1,
            Leg().with_target(v1).with_xy(-1, 0).with_type("line").with_incoming(),
            Leg().with_target(v1).with_xy(1, -1).with_type("line").with_incoming(),
            Leg().with_target(v1).with_xy(1, 1).with_type("line").with_outgoing(),
        )

        self.set_feynman_diagram(fd)
        self.render(show=show)
