from pylatexenc.latex2text import LatexNodes2Text

from pyfeyn2.render.text.ascii import ASCIIRender, Label
from pyfeyn2.render.text.line import ASCIILine
from pyfeyn2.render.text.style import Compass


class ULabel(Label):
    def handle_tex(self, s):
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


class UnicodeRender(ASCIIRender):
    """Renders Feynman diagrams to Unicode art."""

    namedlines = {
        **ASCIIRender.namedlines,
        "label": ULabel,
        "fermion": UFermion,
    }
