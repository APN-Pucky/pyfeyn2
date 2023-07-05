from pathlib import Path

from feynml.feynmandiagram import FeynmanDiagram
from feynml.leg import Leg
from feynml.propagator import Propagator
from feynml.vertex import Vertex
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig


def test_print_as_xml():
    fd = FeynmanDiagram()
    v1 = Vertex("v1")
    v2 = Vertex("v2")
    p1 = Propagator("p1")
    l1 = Leg("l1")
    p1.with_source(v1)
    p1.with_target(v2)
    fd.propagators.append(p1)
    fd.vertices.append(v1)
    fd.vertices.append(v2)
    fd.legs.append(l1)

    config = SerializerConfig(pretty_print=True)
    serializer = XmlSerializer(config=config)
    print(serializer.render(fd))


def test_load_xml():
    xml_string = Path("tests/simple.xml").read_text()
    parser = XmlParser()
    fd = parser.from_string(xml_string, FeynmanDiagram)
    print(fd)


test_print_as_xml()
test_load_xml()
