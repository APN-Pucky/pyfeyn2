import os
import subprocess
import tempfile
from pathlib import Path

from pyfeyn2.render.latex.latex import LatexRender


class MetaPostRender(LatexRender):
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
        temp_dir=None,
    ):
        if temp_dir is None:
            temp_dir = tempfile.TemporaryDirectory()
        super().render(
            file,
            show=False,
            resolution=resolution,
            width=width,
            height=height,
            clean_up=False,
            temp_dir=temp_dir,
        )
        # parent_dir = Path(file if file else "tmp.pdf").parent.absolute()
        parent_dir = temp_dir.name
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
                    cwd=parent_dir,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT,
                )
        ret = super().render(
            file,
            show=show,
            resolution=resolution,
            width=width,
            height=height,
            clean_up=clean_up,
            temp_dir=temp_dir,
        )
        # TODO this should no longer be necessary
        # if clean_up:
        #    for filename in os.listdir(parent_dir):
        #        if filename.endswith(".mp") and filename.startswith("tmp"):
        #            os.remove(Path.joinpath(parent_dir, filename))
        #        elif filename.endswith(".log") and filename.startswith("tmp"):
        #            os.remove(Path.joinpath(parent_dir, filename))
        #        elif filename.endswith(".1") and filename.startswith(
        #            "tmp"
        #        ):  # TODO maybe add more numbers
        #            os.remove(Path.joinpath(parent_dir, filename))
        return ret
