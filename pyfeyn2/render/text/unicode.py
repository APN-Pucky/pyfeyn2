from asciidraw.line import ASCIILine
from asciidraw.point import ASCIIPoint
from asciidraw.style import Compass
from pylatexenc.latex2text import LatexNodes2Text

from pyfeyn2.render.text.ascii import ASCIIRender, Label


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
            style=Compass(
                ww="←",
                ee="→",
                nn="↑",
                ss="↓",
                nw="↖",
                ne="↗",
                sw="↙",
                se="↘",
                begin="*",
                end="*",
            ),
        )


class AntiUFermion(ASCIILine):
    def __init__(self):
        super().__init__(
            style=Compass(
                ee="←",
                ww="→",
                ss="↑",
                nn="↓",
                se="↖",
                nw="↘",
                sw="↗",
                ne="↙",
                begin="*",
                end="*",
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
        "vertical ellipse": ASCIIPoint("⬮"),
        "horizontal ellipse": ASCIIPoint("⬬"),
        "pentagram": ASCIIPoint("⛤"),
        "star": ASCIIPoint("★"),
        "blob": ASCIIPoint("◍"),
    }
