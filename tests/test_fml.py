from pathlib import Path

# Load an FML file and check that it is the same as the original
# FeynmanDiagram object
from feynml.feynmandiagram import FeynmanDiagram
from feynml.feynml import FeynML
from feynml.head import Head
from feynml.leg import Leg
from feynml.meta import Meta
from feynml.momentum import Momentum
from feynml.propagator import Propagator
from feynml.vertex import Vertex
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from pyfeyn2.render.pyx.pyxrender import PyxRender


def test_fml_print():
    fd = FeynmanDiagram()
    v1 = Vertex("v1")
    v2 = Vertex("v2")
    p1 = Propagator("p1")
    l1 = Leg("l1")
    p1.with_source(v1).with_momentum(Momentum("p1", 1, 2, 3, 4))
    p1.with_target(v2)
    fd.propagators.append(p1)
    fd.vertices.append(v1)
    fd.vertices.append(v2)
    fd.legs.append(l1)

    fml = FeynML(
        head=Head(
            metas=[
                Meta(name="pyfeyn2", content="test"),
                Meta(name="description", content="Simple single test diagram"),
            ],
        ),
        diagrams=[fd],
    )
    config = SerializerConfig(pretty_print=True)
    serializer = XmlSerializer(config=config)
    print(serializer.render(fml))


def test_fml_load():
    xml_string = Path("tests/test.fml").read_text()
    parser = XmlParser()
    fd = parser.from_string(xml_string, FeynML)
    print(fd)


def test_fml_plot():
    xml_string = Path("tests/test.fml").read_text()
    parser = XmlParser()
    fml = parser.from_string(xml_string, FeynML)
    PyxRender(fml.diagrams[0]).render()


def test_fml_css():
    xml_string = Path("tests/test.fml").read_text()
    parser = XmlParser()
    fml = parser.from_string(xml_string, FeynML)
    for l in fml.diagrams[0].legs:
        if l.id == "E1":
            if l.style is None:
                continue
            # print(l.raw_style)
            print("NE", l.style.getPropertyValue("arrow-pos"))
            print("NE", l.style.opacity)
            print("NE", l.style.width)
            l.style.opacity = "0.5"
            l.style.width = "40%"
            print("NE", l.style.opacity)
            print(l.style)
            print("tot", l.style.cssText)
    config = SerializerConfig(pretty_print=True)
    serializer = XmlSerializer(config=config)
    print(serializer.render(fml))


test_fml_print()
# test_fml_load()
# test_fml_plot()
# test_fml_css()
