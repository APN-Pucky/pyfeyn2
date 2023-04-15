from typing import List
from warnings import warn

from pyfeyn2.feynmandiagram import Point
from pyfeyn2.render.render import Render
from pyfeyn2.render.text.label import Label
from pyfeyn2.render.text.line import ASCIILine
from pyfeyn2.render.text.point import ASCIIPoint
from pyfeyn2.render.text.style import Cross

try:
    import colorama
    from termcolor import colored
except ImportError:
    warn("colorama and termcolor are required for colored ASCII rendering")

    def colored(text, color):
        return text


class Gluon(ASCIILine):
    def __init__(self, **kwargs):
        super().__init__(
            style=Cross(vert=["O"], horz=["O"]), begin="*", end="*", **kwargs
        )


class Photon(ASCIILine):
    def __init__(self, **kwargs):
        super().__init__(
            begin="*", end="*", style=Cross(vert=["(", ")"], horz=["~"]), **kwargs
        )


class Fermion(ASCIILine):
    def __init__(self, **kwargs):
        super().__init__(
            begin="*",
            end="*",
            style=Cross(
                left="--<--",
                right="-->--",
                up="||^||",
                down="||v||",
            ),
            **kwargs,
        )


class AntiFermion(ASCIILine):
    def __init__(self, **kwargs):
        super().__init__(
            begin="*",
            end="*",
            style=Cross(
                left="-->--",
                right="--<--",
                up="||v||",
                down="||^||",
            ),
            **kwargs,
        )


class Line(ASCIILine):
    def __init__(self, **kwargs):
        super().__init__(
            begin="*",
            end="*",
            style=Cross(
                left="-----",
                right="-----",
                up="|||||",
                down="|||||",
            ),
            **kwargs,
        )


class Scalar(ASCIILine):
    def __init__(self, **kwargs):
        super().__init__(
            begin="*",
            end="*",
            style=Cross(
                left="..<..",
                right="..>..",
                up="::^::",
                down="::v::",
            ),
            **kwargs,
        )


class Ghost(ASCIILine):
    def __init__(self, **kwargs):
        super().__init__(
            begin="*",
            end="*",
            style=Cross(
                vert=":",
                horz=".",
            ),
            **kwargs,
        )


class Higgs(ASCIILine):
    def __init__(self, **kwargs):
        super().__init__(
            begin="*",
            end="*",
            style=Cross(
                vert="=",
                horz="H",
            ),
            **kwargs,
        )


class Gluino(ASCIILine):
    def __init__(self, **kwargs):
        super().__init__(
            begin="*", end="*", style=Cross(vert=["&"], horz=["&"]), **kwargs
        )


class Gaugino(ASCIILine):
    def __init__(self, **kwargs):
        super().__init__(
            begin="*", end="*", style=Cross(vert=["$"], horz=["$"]), **kwargs
        )


class Phantom(ASCIILine):
    def __init__(self, **kwargs):
        super().__init__(begin=None, end=None, style=Cross(vert="", horz=""), **kwargs)

    def draw(self, pane, isrc, itar, scalex=1, scaley=1, kickx=0, kicky=0):
        pass


class ASCIIRender(Render):
    """Renders Feynman diagrams to ASCII art."""

    namedlines = {
        "gluon": Gluon,
        "photon": Photon,
        "vector": Photon,
        "boson": Photon,
        "fermion": Fermion,
        "anti fermion": AntiFermion,
        "ghost": Ghost,
        "higgs": Higgs,
        "scalar": Scalar,
        "slepton": Scalar,
        "squark": Scalar,
        "gluino": Gluino,
        "gaugino": Gaugino,
        "phantom": Phantom,
        "line": Line,
        # TODO what is this?
        "label": Label,
    }

    namedshapes = {
        "dot": ASCIIPoint("."),
        "empty": ASCIIPoint("O"),
        "cross": ASCIIPoint("x"),
        "square": ASCIIPoint("#"),
        "blob": ASCIIPoint("@"),
        "star": ASCIIPoint("*"),
    }

    def __init__(self, fd=None, *args, **kwargs):
        super().__init__(fd, *args, **kwargs)

    def get_color_text(self, text, color):
        return colored(text, color)

    def draw_connector(self, pane, connector, src, tar, fmt):
        """
        Draw a connector between two points.
        """
        p = connector
        tmp_fmt = {}
        pstyle = self.fd.get_style(p)

        if pstyle.getProperty("line") is not None:
            lname = pstyle.getProperty("line").value
        else:
            lname = p.type  # fallback no style
        if pstyle.getProperty("color") is not None:
            tmp_fmt["colorer"] = lambda t: self.get_color_text(
                t, pstyle.getProperty("color").value
            )
        self.namedlines[lname]().draw(pane, src, tar, **fmt, **tmp_fmt)
        if p.label is not None:
            tmp_fmt = {}
            if pstyle.getProperty("label-color") is not None:
                tmp_fmt["colorer"] = lambda t: self.get_color_text(
                    t, pstyle.getProperty("label-color").value
                )
            self.namedlines["label"](p.label).draw(pane, src, tar, **fmt, **tmp_fmt)

    def render(
        self,
        file=None,
        show=True,
        resolution=100,
        width=None,
        height=None,
        clean_up=True,
    ):
        minx, miny, maxx, maxy = self.fd.get_bounding_box()

        shift = 2
        # maxx = maxx + shift
        maxy = maxy + shift
        # minx = minx - shift
        miny = miny - shift

        if width is None:
            width = int((maxx - minx) * resolution / 10)
        if height is None:
            height = int(
                (maxy - miny) * resolution / 10 / 2
            )  # divide by two to make it look better due to aspect ratio

        pane = []
        for _ in range(height):
            pane.append([" "] * width)

        scalex = (width - 1) / (maxx - minx)
        scaley = -(height - 1) / (maxy - miny)
        kickx = -minx
        kicky = -maxy
        fmt = {"scalex": scalex, "kickx": kickx, "scaley": scaley, "kicky": kicky}

        for p in self.fd.propagators:
            src = self.fd.get_vertex(p.source)
            tar = self.fd.get_vertex(p.target)
            self.draw_connector(pane, p, src, tar, fmt)

        for l in self.fd.legs:
            if l.is_incoming():
                src = Point(l.x, l.y)
                tar = self.fd.get_vertex(l.target)
                self.draw_connector(pane, l, src, tar, fmt)
            elif l.is_outgoing():
                src = self.fd.get_vertex(l.target)
                tar = Point(l.x, l.y)
                self.draw_connector(pane, l, src, tar, fmt)
        for v in self.fd.vertices:
            tmp_fmt = {}
            ssss = self.fd.get_style(v)
            if ssss.getProperty("symbol") is not None:
                if ssss.getProperty("color") is not None:
                    tmp_fmt["colorer"] = lambda t: self.get_color_text(
                        t, ssss.getProperty("color").value
                    )
                self.namedshapes[ssss.getProperty("symbol").value].draw(
                    pane, v, **fmt, **tmp_fmt
                )
            if v.label is not None:
                tmp_fmt = {}
                if ssss.getProperty("label-color") is not None:
                    tmp_fmt["colorer"] = lambda t: self.get_color_text(
                        t, ssss.getProperty("label-color").value
                    )
                self.namedlines["label"](v.label).draw(
                    pane,
                    Point(v.x - len(v.label) / 2, v.y),
                    Point(v.x + len(v.label) / 2, v.y),
                    **fmt,
                    **tmp_fmt,
                )

        joined = "\n".join(["".join(row) for row in pane]) + "\n"
        self.set_src_txt(joined)
        if file:
            # warn("Writing with color tags to file. Disable with NO_COLOR=1 env var")
            with open(file, "w") as f:
                f.write(joined)
        if show:
            print(joined)
        return joined

    def get_src_txt(self):
        return self.src_txt

    def set_src_txt(self, src_txt):
        self.src_txt = src_txt

    @classmethod
    def valid_attributes(cls) -> List[str]:
        return super(ASCIIRender, cls).valid_attributes() + [
            "x",
            "y",
            "label",
            "style",
        ]

    @classmethod
    def valid_styles(cls) -> List[str]:
        return super(ASCIIRender, cls).valid_styles() + [
            "line",
            "symbol",
            "color",
            "label-color",
        ]

    @classmethod
    def valid_types(cls) -> List[str]:
        return super(ASCIIRender, cls).valid_types() + list(
            ASCIIRender.namedlines.keys()
        )

    @classmethod
    def valid_shapes(cls) -> List[str]:
        return super(ASCIIRender, cls).valid_types() + list(
            ASCIIRender.namedshapes.keys()
        )
