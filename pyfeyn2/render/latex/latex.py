import os
import re
import tempfile
from pathlib import Path

from IPython.display import display
from pylatex import Document
from pylatex.utils import NoEscape
from wand.image import Image as WImage

from pyfeyn2.render.render import Render


class LatexRender(Document, Render):
    def __init__(
        self,
        fd=None,
        documentclass="standalone",
        document_options=None,
        *args,
        **kwargs,
    ):
        if document_options is None:
            document_options = ["preview", "crop"]
        super().__init__(
            *args,
            documentclass=documentclass,
            document_options=document_options,
            **kwargs,
        )
        Render.__init__(self, fd)

    def get_src(self):
        return self.dumps()

    def get_src_diag(self):
        return self.src_diag

    def set_src_diag(self, src_diag):
        self.src_diag = src_diag
        self.append(NoEscape(src_diag))

    def render(
        self,
        file=None,
        show=True,
        resolution=100,
        width=None,
        height=None,
        clean_up=True,
        temp_dir=None,
    ):
        if temp_dir is None:
            temp_dir = tempfile.TemporaryDirectory()
        delete = False
        if file is None:
            delete = True
            file = "tmp"
        file = re.sub(r"\.pdf$", "", file.strip())
        tfile = re.sub(r"\.pdf$", "", os.path.basename(file).strip())
        tfile = os.path.join(temp_dir.name, tfile)
        self.generate_pdf(
            tfile,
            clean_tex=clean_up,
            compiler="lualatex",
            compiler_args=["-shell-escape"],
        )
        wi = WImage(
            filename=tfile + ".pdf", resolution=resolution, width=width, height=height
        )
        if file is not None:
            # Copy tfile to file
            Path(file).parent.mkdir(parents=True, exist_ok=True)
            os.rename(tfile + ".pdf", file)
        if delete:
            os.remove(tfile + ".pdf")
        if clean_up and temp_dir:
            temp_dir.cleanup()
        if show:
            display(wi)
        return wi
