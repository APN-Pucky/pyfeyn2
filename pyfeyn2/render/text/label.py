import copy
import re

from pyfeyn2.render.text.line import ASCIILine
from pyfeyn2.render.text.style import Cross


class Label(ASCIILine):
    def __init__(self, label, handle_tex=True):
        if handle_tex:
            self.label = self.handle_tex(label)
        else:
            self.label = label
        super().__init__(
            begin=None,
            end=None,
            style=Cross(
                vert=[*self.label, None], horz=[*self.label, None], terminate=True
            ),
        )

    @staticmethod
    def handle_tex(s):
        """
        Remove TeX commands from a string to pure ASCII.
        """
        s = s.replace("\\bar", "_")
        s = s.replace("\\tilde", "~")
        s = re.sub(r"\\[a-zA-Z]+", "", s)
        return (
            s.replace("$", "")
            .replace("{", "")
            .replace("}", "")
            .replace("\\(", "")
            .replace("\\)", "")
            .replace("\\", "")
            .replace("^", "")
        )

    def draw(
        self,
        pane,
        isrc,
        itar,
        scalex=1,
        scaley=1,
        kickx=0,
        kicky=0,
        colorer=lambda x: x,
        **kwargs
    ):
        jsrc = copy.copy(isrc)
        jtar = copy.copy(itar)

        # reduce length to 1/3 in the middle
        jsrc.x = (itar.x - isrc.x) / 3.0 + isrc.x
        jsrc.y = (itar.y - isrc.y) / 3.0 + isrc.y
        jtar.x = (itar.x - isrc.x) / 3.0 * 2.0 + isrc.x
        jtar.y = (itar.y - isrc.y) / 3.0 * 2.0 + isrc.y

        ## shift the line
        shift = 3.0
        # horizonral
        if abs(isrc.x - itar.x) > abs(isrc.y - itar.y):
            # left to right -> shift up
            if isrc.x < itar.x:
                jsrc.y -= shift / scaley
                jtar.y -= shift / scaley
            # right to left -> shift down
            else:
                jsrc.y += shift / scaley
                jtar.y += shift / scaley

        # vertical
        else:
            # up to down -> shift left
            if isrc.y < itar.y:
                jsrc.x -= shift / scalex
                jtar.x -= shift / scalex
            # down to up -> shift right
            else:
                jsrc.x += shift / scalex
                jtar.x += shift / scalex

        super().draw(pane, jsrc, jtar, scalex, scaley, kickx, kicky, colorer, **kwargs)
        self.index = 0
