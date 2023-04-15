# TODO read in FeynMF and produce pdf output allowing to choose renderer
import argparse
import importlib
from pathlib import Path

from feynml.feynml import FeynML
from xsdata.formats.dataclass.parsers import XmlParser

import pyfeyn2.render.all as all


def class_for_name(module_name, class_name):
    # load the module, will raise ImportError if module cannot be loaded
    m = importlib.import_module(module_name)
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, class_name)
    return c


def renderer_from_string(s):
    return class_for_name(".".join(s.split(".")[0:-1]), s.split(".")[-1])


def main():
    # parse command line options with argparse
    parser = argparse.ArgumentParser(
        prog="pyfeyn2.mkfeyndiag",
        description="Draw FeynML diagrams with pyfeyn2.",
    )
    parser.add_argument(
        "input",
        metavar="INPUT",
        type=str,
        help="Input FeynML file.",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="OUTPUT",
        default="output.pdf",
        type=str,
        help="Output file.",
    )
    parser.add_argument(
        "-r",
        "--renderer",
        metavar="RENDERER",
        default=None,
        type=str,
        help="Renderer to use.",
    )

    args = parser.parse_args()

    arenderer = args.renderer
    renderer = None
    if arenderer is None:
        pass
    elif arenderer.lower() in all.renders:
        renderer = all.renders[arenderer.lower()]
    else:
        renderer = renderer_from_string(arenderer)

    xml_string = Path(args.input).read_text()
    parser = XmlParser()
    fml = parser.from_string(xml_string, FeynML)

    if renderer is None:
        arenderer = fml.head.get_meta_dict()["renderer"]
        renderer = renderer_from_string(arenderer)

    # TODO think about how to handle multiple diagrams
    renderer(fml.diagrams[0]).render(file=args.output)
