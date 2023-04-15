from pylatex import Command
from pylatex.utils import NoEscape

from pyfeyn2.render.text.plainpdf import PlainPDFRender
from pyfeyn2.render.text.unicode import UnicodeRender


class UnicodePDFRender(PlainPDFRender, UnicodeRender):
    """Renders Feynman diagrams as Unicode art to PDF."""

    def __init__(
        self,
        *args,
        document_options=None,
        environment="minted",
        environment_arg="text",
        **kwargs,
    ):
        if document_options is None:
            document_options = ["preview"]
        UnicodeRender.__init__(self, *args, **kwargs)
        PlainPDFRender.__init__(
            self,
            *args,
            document_options=document_options,
            environment=environment,
            environment_arg=environment_arg,
            **kwargs,
        )

        self.preamble.append(Command("usepackage", NoEscape("fontspec")))

        self.preamble.append(Command("usepackage", NoEscape("minted")))

        # self.preamble.append(Command("setmonofont", NoEscape("Courier New") , "Scale=0.9"))
        self.preamble.append(
            NoEscape(
                r"""
\setmonofont{LiberationMono}[
  Extension=.ttf,
  UprightFont=*-Regular,
  ItalicFont=*-Italic,
  BoldFont=*-Bold,
  BoldItalicFont=*-BoldItalic,
]

\frenchspacing
            """
            )
        )
        # self.usepackage("libertine")
        # \setmainfont{Linux Libertine O}
        # self.preamble.append(Command("setmainfont", NoEscape("Linux Liberine O")))

    def render(
        self,
        file=None,
        show=True,
        resolution=100,
        width=None,
        height=None,
        clean_up=True,
    ):
        UnicodeRender.render(
            self,
            file=None,
            show=False,
            resolution=resolution,
            width=width,
            height=height,
        )
        return PlainPDFRender.render(
            self, file, show, resolution, width, height, clean_up
        )
