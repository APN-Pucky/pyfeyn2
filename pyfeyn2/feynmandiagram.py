"""Moved to :py:mod:`feynml`"""
from importlib.metadata import version

from feynml.connector import Connector as Connector_
from feynml.feynmandiagram import FeynmanDiagram as FeynmanDiagram_
from feynml.feynml import FeynML as FeynML_
from feynml.feynml import Head as Head_
from feynml.feynml import Meta as Meta_
from feynml.feynml import Tool as Tool_
from feynml.leg import Leg as Leg_
from feynml.momentum import Momentum as Momentum_
from feynml.pdgid import PDG as PDG_
from feynml.point import Point as Point_
from feynml.propagator import Propagator as Propagator_
from feynml.styled import Styled as Styled_
from feynml.vertex import Vertex as Vertex_
from smpl_doc import doc


class Head(Head_):
    class Meta(Head_.Meta):
        pass

    @doc.deprecated("2.2.6", "Directly use feynml.feynml.Head")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Meta(Meta_):
    class Meta(Meta_.Meta):
        pass

    @doc.deprecated("2.2.6", "Directly use feynml.feynml.Meta")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Tool(Tool_):
    class Meta(Tool_.Meta):
        pass

    @doc.deprecated("2.2.6", "Directly use feynml.feynml.Tool")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Connector(Connector_):
    @doc.deprecated("2.2.6", "Directly use feynml.connector.Connector")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class FeynmanDiagram(FeynmanDiagram_):
    class Meta(FeynmanDiagram_.Meta):
        pass

    @doc.deprecated("2.2.6", "Directly use feynml.feynmandiagram.FeynDiagram")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Leg(Leg_):
    @doc.deprecated("2.2.6", "Directly use feynml.leg.Leg")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Momentum(Momentum_):
    class Meta(Momentum_.Meta):
        pass

    @doc.deprecated("2.2.6", "Directly use feynml.momentum.Momentum")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PDG(PDG_):
    @doc.deprecated("2.2.6", "Directly use feynml.pdgid.PDG")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Vertex(Vertex_):
    @doc.deprecated("2.2.6", "Directly use feynml.vertex.Vertex")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Styled(Styled_):
    @doc.deprecated("2.2.6", "Directly use feynml.styled.Styled")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Propagator(Propagator_):
    @doc.deprecated("2.2.6", "Directly use feynml.propagator.Propagator")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Point(Point_):
    @doc.deprecated("2.2.6", "Directly use feynml.point.Point")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# @doc.deprecated("2.2.6", "Directly use feynml.feynml.FeynML")
class FeynML(FeynML_):
    """FeynML with pyfeyn2 meta tag."""

    class Meta(FeynML_.Meta):
        pass

    def __post_init__(self):
        self.head.metas.append(Meta("pyfeyn2", version("pyfeyn2")))
        return super().__post_init__()
