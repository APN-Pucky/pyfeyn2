from feynman import Diagram
from matplotlib import pyplot as plt

from pyfeyn2.render.render import Render

namedlines = {
    "straight": [{"style": "simple", "arrow": False}],
    "gluon": [
        {"style": "loopy", "arrow": False, "xamp": 0.025, "yamp": 0.035, "nloops": 7}
    ],
    "gluino": [
        {"style": "loopy", "arrow": False, "xamp": 0.025, "yamp": 0.035, "nloops": 7},
        {"style": "simple", "arrow": False},
    ],
    "photon": [{"style": "wiggly", "arrow": False}],
    "boson": [{"style": "wiggly", "arrow": False}],
    "ghost": [{"style": "dashed", "arrow": False}],
    "fermion": [{"style": "simple", "arrow": True}],
    "higgs": [{"style": "dashed", "arrow": False}],
    "gaugino": [
        {"style": "wiggly", "arrow": False},
        {"style": "simple", "arrow": False},
    ],
    "phantom": [],
}


class FeynmanRender(Render):
    def __init__(self, fd=None, *args, **kwargs):
        super().__init__(fd, *args, **kwargs)

    def render(
        self,
        file=None,
        show=True,
        resolution=100,
        width=10.0,
        height=10.0,
        clean_up=True,
    ):
        buffer = 0.9
        # normaliuze to 1
        maxx = minx = maxy = miny = 0.0
        for l in self.fd.legs:
            if l.x < minx:
                minx = l.x
            if l.x > maxx:
                maxx = l.x
            if l.y < miny:
                miny = l.y
            if l.y > maxy:
                maxy = l.y
        for l in self.fd.vertices:
            if l.x < minx:
                minx = l.x
            if l.x > maxx:
                maxx = l.x
            if l.y < miny:
                miny = l.y
            if l.y > maxy:
                maxy = l.y

        kickx = -minx
        kicky = -miny
        scalex = 1.0 / (maxx - minx) * buffer
        scaley = 1.0 / (maxy - miny) * buffer

        fig = plt.figure(figsize=(width, height))
        ax = fig.add_axes([0, 0, 1, 1], frameon=False)
        diagram = Diagram(ax)
        byid = {}
        for v in self.fd.vertices:
            byid[v.id] = diagram.vertex(
                xy=((v.x + kickx) * scalex, (v.y + kicky) * scaley)
            )
        for v in self.fd.legs:
            byid[v.id] = diagram.vertex(
                xy=((v.x + kickx) * scalex, (v.y + kicky) * scaley), marker=""
            )

        for p in self.fd.propagators:
            for style in namedlines[p.type]:
                cur = diagram.line(byid[p.source], byid[p.target], **style)
            if p.label is not None:
                cur.text(p.label)
        for l in self.fd.legs:
            for style in namedlines[l.type]:
                if l.sense[:2] == "in":
                    cur = diagram.line(byid[l.id], byid[l.target], **style)
                elif l.sense[:3] == "out":
                    cur = diagram.line(byid[l.target], byid[l.id], **style)
                else:
                    raise Exception("Unknown sense")
            if l.label is not None:
                cur.text(l.label)

        for l in self.fd.labels:
            diagram.text(
                l.x,
                l.y,
                l.text,
            )
        diagram.plot()
        if show:
            plt.show()
        if file is not None:
            plt.savefig(file)
        if clean_up:
            plt.close()

    @staticmethod
    def valid_attribute(attr: str) -> bool:
        return super(FeynmanRender,FeynmanRender).valid_attribute(attr) or attr in ["x", "y", "label"]

    @staticmethod
    def valid_type(typ: str) -> bool:
        if typ.lower() in namedlines:
            return True
        return False
