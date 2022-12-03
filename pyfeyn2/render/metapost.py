import os
import subprocess
from pathlib import Path

from pyfeyn2.render.latex import LatexRender


class MetaPostRender(LatexRender):
    def __init__(
        self,
        fd,
        documentclass="standalone",
        document_options=["preview", "crop"],
        *args,
        **kwargs,
    ):
        super().__init__(
            *args,
            fd=fd,
            documentclass=documentclass,
            document_options=document_options,
            **kwargs,
        )

    def render(
        self,
        file=None,
        show=True,
        resolution=100,
        width=None,
        height=None,
        clean_up=True,
    ):
        super().render(
            file,
            show=False,
            resolution=resolution,
            width=width,
            height=height,
            clean_up=False,
        )
        parent_dir = (
            os.path.dirname(file) if file else Path("tmp.pdf").parent.absolute()
        )
        # for filename in os.listdir(parent_dir):
        #    if filename.endswith(".dvi"):
        #        os.remove(filename)
        # get parent directory of file
        # execute metapost on every .mp file in parent directory
        for filename in os.listdir(parent_dir):
            # TODO grep src for mp files
            if filename.endswith(".mp") and filename.startswith("tmp"):
                subprocess.call(
                    ["mpost", filename],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT,
                )
        return super().render(
            file,
            show=show,
            resolution=resolution,
            width=width,
            height=height,
            clean_up=clean_up,
        )
