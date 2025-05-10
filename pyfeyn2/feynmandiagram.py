"""Moved to :py:mod:`feynml`"""
from importlib.metadata import version

# from feynml.feynml import Tool as Tool_
from feynml import PDG as PDG_
from feynml import Connector as Connector_
from feynml import FeynmanDiagram as FeynmanDiagram_
from feynml import FeynML as FeynML_
from feynml import Head as Head_
from feynml import Leg as Leg_
from feynml import Meta as Meta_
from feynml import Point as Point_
from feynml import Propagator as Propagator_
from feynml import Styled as Styled_
from feynml import Vertex as Vertex_
from feynml.momentum import Momentum as Momentum_  # TODO fix to feynml only
from smpl_doc.doc import deprecated


class Head(Head_):
    class Meta(Head_.Meta):
        pass

    @deprecated("2.2.6", "Directly use feynml.head.Head")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Meta(Meta_):
    class Meta(Meta_.Meta):
        pass

    @deprecated("2.2.6", "Directly use feynml.meta.Meta")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# class Tool(Tool_):
#    class Meta(Tool_.Meta):
#        pass
#
#    @deprecated("2.2.6", "Directly use feynml.feynml.Tool")
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)


class Connector(Connector_):
    @deprecated("2.2.6", "Directly use feynml.connector.Connector")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class FeynmanDiagram(FeynmanDiagram_):
    class Meta(FeynmanDiagram_.Meta):
        pass

    @deprecated("2.2.6", "Directly use feynml.feynmandiagram.FeynDiagram")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Leg(Leg_):
    @deprecated("2.2.6", "Directly use feynml.leg.Leg")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Momentum(Momentum_):
    class Meta(Momentum_.Meta):
        pass

    @deprecated("2.2.6", "Directly use feynml.momentum.Momentum")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PDG(PDG_):
    @deprecated("2.2.6", "Directly use feynml.pdgid.PDG")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Vertex(Vertex_):
    @deprecated("2.2.6", "Directly use feynml.vertex.Vertex")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Styled(Styled_):
    @deprecated("2.2.6", "Directly use feynml.styled.Styled")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Propagator(Propagator_):
    @deprecated("2.2.6", "Directly use feynml.propagator.Propagator")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Point(Point_):
    @deprecated("2.2.6", "Directly use feynml.point.Point")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# @deprecated("2.2.6", "Directly use feynml.feynml.FeynML")
class FeynML(FeynML_):
    """FeynML with pyfeyn2 meta tag."""

    class Meta(FeynML_.Meta):
        pass

    def __post_init__(self):
        self.head.metas.append(Meta_("pyfeyn2", version("pyfeyn2")))
        return super().__post_init__()
