from pyfeyn2.feynmandiagram import Point
from pyfeyn2.render.render import Render
from pyfeyn2.render.text.label import Label
from pyfeyn2.render.text.line import ASCIILine
from pyfeyn2.render.text.style import Cross


class Gluon(ASCIILine):
    def __init__(self):
        super().__init__(style=Cross(vert=["O"], horz=["O"]), begin="*", end="*")


class Photon(ASCIILine):
    def __init__(self):
        super().__init__(begin="*", end="*", style=Cross(vert=["(", ")"], horz=["~"]))


class Fermion(ASCIILine):
    def __init__(self):
        super().__init__(
            begin="*",
            end="*",
            style=Cross(
                left="--<--",
                right="-->--",
                up="||^||",
                down="||v||",
            ),
        )


class Scalar(ASCIILine):
    def __init__(self):
        super().__init__(
            begin="*",
            end="*",
            style=Cross(
                left="..<..",
                right="..>..",
                up="::^::",
                down="::v::",
            ),
        )


class Ghost(ASCIILine):
    def __init__(self):
        super().__init__(
            begin="*",
            end="*",
            style=Cross(
                vert=":",
                horz=".",
            ),
        )


class Higgs(ASCIILine):
    def __init__(self):
        super().__init__(
            begin="*",
            end="*",
            style=Cross(
                vert="=",
                horz="H",
            ),
        )


class Gluino(ASCIILine):
    def __init__(self):
        super().__init__(begin="*", end="*", style=Cross(vert=["&"], horz=["&"]))


class Gaugino(ASCIILine):
    def __init__(self):
        super().__init__(begin="*", end="*", style=Cross(vert=["$"], horz=["$"]))


class Phantom(ASCIILine):
    def __init__(self):
        super().__init__(begin=None, end=None, style=Cross(vert="", horz=""))

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
        "ghost": Ghost,
        "higgs": Higgs,
        "scalar": Scalar,
        "slepton": Scalar,
        "squark": Scalar,
        "gluino": Gluino,
        "gaugino": Gaugino,
        "phantom": Phantom,
        "label": Label,
    }

    def __init__(self, fd=None, *args, **kwargs):
        super().__init__(fd, *args, **kwargs)

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
            src = self.fd.get_point(p.source)
            tar = self.fd.get_point(p.target)
            self.namedlines[p.type]().draw(pane, src, tar, **fmt)
            if p.label is not None:
                self.namedlines["label"](p.label).draw(pane, src, tar, **fmt)
        for l in self.fd.legs:
            tar = self.fd.get_point(l.target)
            if l.sense[:2] == "in" or l.sense[:8] == "anti-out":
                self.namedlines[l.type]().draw(pane, Point(l.x, l.y), tar, **fmt)
                if l.label is not None:
                    self.namedlines["label"](l.label).draw(
                        pane, Point(l.x, l.y), tar, **fmt
                    )
            elif l.sense[:3] == "out" or l.sense[:9] == "anti-in":
                self.namedlines[l.type]().draw(pane, tar, Point(l.x, l.y), **fmt)
                if l.label is not None:
                    self.namedlines["label"](l.label).draw(
                        pane, tar, Point(l.x, l.y), **fmt
                    )

        joined = "\n".join(["".join(row) for row in pane]) + "\n"
        self.set_src_txt(joined)
        if show:
            print(joined)
        return joined

    def get_src_txt(self):
        return self.src_txt

    def set_src_txt(self, src_txt):
        self.src_txt = src_txt

    @staticmethod
    def valid_attribute(attr: str) -> bool:
        return super(ASCIIRender, ASCIIRender).valid_attribute(attr) or attr in [
            "x",
            "y",
            "label",
        ]

    @staticmethod
    def valid_type(typ: str) -> bool:
        if typ.lower() in ASCIIRender.namedlines:
            return True
        return False
