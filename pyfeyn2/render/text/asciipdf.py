from pyfeyn2.render.text.ascii import ASCIIRender
from pyfeyn2.render.text.plainpdf import PlainPDFRender


class ASCIIPDFRender(PlainPDFRender, ASCIIRender):
    """Renders Feynman diagrams as ASCII art to PDF."""

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        ASCIIRender.__init__(self, *args, **kwargs)
        PlainPDFRender.__init__(self, *args, **kwargs)

    def render(
        self,
        file=None,
        show=True,
        resolution=100,
        width=None,
        height=None,
        clean_up=True,
    ):
        ASCIIRender.render(
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
