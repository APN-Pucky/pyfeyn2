from pylatex import Command
from pylatex.utils import NoEscape

from pyfeyn2.render.latex.latex import LatexRender


class PlainPDFRender(LatexRender):
    """Renders Feynman diagrams as ASCII art to PDF."""

    def __init__(
        self,
        fd=None,
        documentclass="standalone",
        document_options=None,
        environment="lstlisting",
        environment_arg=None,
        *args,
        **kwargs,
    ):
        if document_options is None:
            document_options = ["preview", "crop"]
        super().__init__(
            fd,
            documentclass=documentclass,
            document_options=document_options,
            *args,
            **kwargs,
        )
        self.preamble.append(Command("usepackage", NoEscape("listings")))
        self.preamble.append(Command("usepackage", NoEscape("xcolor")))
        self.environment = environment
        self.environment_arg = environment_arg

    def get_color_text(self, text, color):
        """
        Return text with color via LaTeX commands.
        """
        self.preamble.append(
            Command(
                "lstset",
                NoEscape(
                    "moredelim=[is][\color{"
                    + color
                    + "}]{@"
                    + color
                    + "!}{!"
                    + color
                    + "@}"
                ),
            )
        )
        return "@" + color + "!" + text + "!" + color + "@"

    def render(
        self,
        file=None,
        show=True,
        resolution=100,
        width=None,
        height=None,
        clean_up=True,
    ):
        # str = T.render(self, None, False, resolution, width, height)
        self.set_src_diag(
            f"\\begin{{{self.environment}}}"
            + (
                f"{{{self.environment_arg}}}"
                if self.environment_arg is not None
                else ""
            )
            + "\n"
            + self.src_txt
            + f"\\end{{{self.environment}}}\n"
        )
        LatexRender.render(self, file, show, resolution, width, height, clean_up)
