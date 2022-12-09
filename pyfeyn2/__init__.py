from pyfeyn2.render.ascii import ASCIIRender
from pyfeyn2.render.dot import DotRender
from pyfeyn2.render.feynmp import FeynmpRender
from pyfeyn2.render.mpl import MPLRender
from pyfeyn2.render.pyx.pyxrender import PyxRender
from pyfeyn2.render.tikzfeynman import TikzFeynmanRender

renders = {
    "pyx": PyxRender,
    "dot": DotRender,
    "ascii": ASCIIRender,
    "mpl": MPLRender,
    "feynmp": FeynmpRender,
    "tikzfeynman": TikzFeynmanRender,
}
styles = ["arrow-pos", "parallel-arrow-sense", "parallel-arrow-displace"]
types = [
    # General
    "fermion",
    "boson",
    "vector",
    "scalar",
    # SM
    "photon",
    "higgs",
    "gluon",
    "ghost",
    # Grav
    "graviton",
    # MSSM
    "gluino",
    "squark",
    "slepton",
    "gaugino",
    "neutralino",
    "chargino",
    "higgsino",
    "gravitino",
]
attributes = [
    "x",
    "y",
    "bend",
    "label",
    "pdgid",
    "sense",
    "target",
    "source",
    "style",
    "id",
    "type",
    "text",
]
