from feynml.feynmandiagram import FeynmanDiagram
from feynml.leg import Leg
from feynml.propagator import Propagator
from feynml.vertex import Vertex
from matplotlib import pyplot as plt

from pyfeyn2.render.all import AllRender


def test_all_demo_propagator():
    for prop in AllRender.valid_types():
        AllRender().demo_propagator(prop, show=False)
        plt.close()


def test_all_2_to_2_gluons():
    fd = FeynmanDiagram()
    v1 = Vertex("v1").with_xy(-1, 0)
    v2 = Vertex("v2").with_xy(1, 0)
    p1 = Propagator("p1").connect(v1, v2).with_type("gluon")
    l1 = Leg("l1").with_target(v1).with_xy(-2, 1).with_type("gluon").with_incoming()
    l2 = Leg("l2").with_target(v1).with_xy(-2, -1).with_type("gluon").with_incoming()
    l3 = Leg("l3").with_target(v2).with_xy(2, 1).with_type("gluon").with_outgoing()
    l4 = Leg("l4").with_target(v2).with_xy(2, -1).with_type("gluon").with_outgoing()
    p1.with_source(v1)
    p1.with_target(v2)
    fd.propagators.append(p1)
    fd.vertices.extend([v1, v2])
    fd.legs.extend([l1, l2, l3, l4])
    AllRender(fd).render()
