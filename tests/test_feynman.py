from feynml.feynmandiagram import FeynmanDiagram
from feynml.leg import Leg
from feynml.propagator import Propagator
from feynml.vertex import Vertex


def get_test_gluons():
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
    return fd


def get_test_many_gluons():
    fd = FeynmanDiagram()
    v1 = Vertex("v1")
    v2 = Vertex("v2")
    v3 = Vertex("v3")
    v4 = Vertex("v4")
    p1 = Propagator("p1").connect(v1, v2).with_type("gluon")
    p2 = Propagator("p2").connect(v1, v3).with_type("gluon")
    p3 = Propagator("p3").connect(v3, v2).with_type("gluon")
    p4 = Propagator("p4").connect(v4, v3).with_type("gluon")
    p5 = Propagator("p5").connect(v4, v2).with_type("gluon")
    l1 = Leg("l1").with_target(v1).with_type("gluon").with_incoming().with_xy(-2, 1)
    l2 = Leg("l2").with_target(v1).with_type("gluon").with_incoming().with_xy(-2, -1)
    l3 = Leg("l3").with_target(v2).with_type("gluon").with_outgoing().with_xy(2, -2)
    l4 = Leg("l4").with_target(v3).with_type("gluon").with_outgoing().with_xy(2, 2)
    l5 = Leg("l5").with_target(v4).with_type("gluon").with_outgoing().with_xy(2, 1)
    l6 = Leg("l6").with_target(v4).with_type("gluon").with_outgoing().with_xy(2, -1)

    fd.propagators.extend([p1, p2, p3, p4, p5])
    fd.vertices.extend([v1, v2, v3, v4])
    fd.legs.extend([l1, l2, l3, l4, l5, l6])
    return fd
