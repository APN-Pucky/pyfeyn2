from pylatexenc.latex2text import LatexNodes2Text

from pyfeyn2.render.text.ascii import ASCIIRender, Label
from pyfeyn2.render.text.line import ASCIILine
from pyfeyn2.render.text.point import ASCIIPoint
from pyfeyn2.render.text.style import Compass


class ULabel(Label):
    @staticmethod
    def handle_tex(s):
        """
        Converts LaTeX to unicode.
        """
        ret = LatexNodes2Text().latex_to_text(s)
        return ret


class UFermion(ASCIILine):
    def __init__(self):
        super().__init__(
            begin="*",
            end="*",
            style=Compass(
                ww="←",
                ee="→",
                nn="↑",
                ss="↓",
                nw="↖",
                ne="↗",
                sw="↙",
                se="↘",
            ),
        )


class AntiUFermion(ASCIILine):
    def __init__(self):
        super().__init__(
            begin="*",
            end="*",
            style=Compass(
                ee="←",
                ww="→",
                ss="↑",
                nn="↓",
                se="↖",
                nw="↘",
                sw="↗",
                ne="↙",
            ),
        )


class UnicodeRender(ASCIIRender):
    """Renders Feynman diagrams to Unicode art."""

    namedlines = {
        **ASCIIRender.namedlines,
        "label": ULabel,
        "fermion": UFermion,
        "anti fermion": AntiUFermion,
    }

    namedshapes = {
        **ASCIIRender.namedshapes,
        "triangle": ASCIIPoint("▲"),
        "square": ASCIIPoint("■"),
        "dot": ASCIIPoint("●"),
        "diamond": ASCIIPoint("◆"),
        "pentagram": ASCIIPoint("⛤"),
        "star": ASCIIPoint("★"),
        "blob": ASCIIPoint("◍"),
    }
