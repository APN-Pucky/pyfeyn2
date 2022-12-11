import matplotlib.pyplot as plt
import numpy as np

from pyfeyn2.render.render import Render


def dotted(p1, p2, points=200):
    n = np.linspace(0, points, points)
    x, y = (
        p1[0] + (p2[0] - p1[0]) * (n / points),
        p1[1] + (p2[1] - p1[1]) * (n / points),
    )
    plt.plot(x, y, "k:")


def dashed(p1, p2, points=200):
    n = np.linspace(0, points, points)
    x, y = (
        p1[0] + (p2[0] - p1[0]) * (n / points),
        p1[1] + (p2[1] - p1[1]) * (n / points),
    )
    plt.plot(x, y, "k--")


def line(p1, p2, points=200):
    n = np.linspace(0, points, points)
    x, y = (
        p1[0] + (p2[0] - p1[0]) * (n / points),
        p1[1] + (p2[1] - p1[1]) * (n / points),
    )
    plt.plot(x, y, "k-")


def spring(xp1, xp2, points=200, rot=3, amp=0.15, line_frac=0.2):
    p1 = [
        xp1[0] + (xp2[0] - xp1[0]) * line_frac,
        xp1[1] + (xp2[1] - xp1[1]) * line_frac,
    ]

    p2 = [
        xp2[0] - (xp2[0] - xp1[0]) * line_frac,
        xp2[1] - (xp2[1] - xp1[1]) * line_frac,
    ]

    n = np.linspace(0, points, points)
    alpha = np.arctan((p2[1] - p1[1]) / np.array([(p2[0] - p1[0])]))
    if p2[0] < p1[0]:
        alpha += np.pi
    w = rot / points * (2 * np.pi) + np.pi / points
    ret = (
        p1[0]
        + (p2[0] - p1[0]) * (n / points)
        + amp * (-np.cos(w * n - alpha) + np.cos(-alpha)),
        p1[1]
        + (p2[1] - p1[1]) * (n / points)
        + amp * (np.sin(w * n - alpha) - np.sin(-alpha)),
    )

    x, y = (
        np.append(np.insert(ret[0], 0, xp1[0]), xp2[0]),
        np.append(np.insert(ret[1], 0, xp1[1]), xp2[1]),
    )
    plt.plot(x, y, "k-")


def wave(xp1, xp2, points=200, rot=3, amp=0.15, line_frac=0.2):
    # first skip via p1 and p2 to
    p1 = [
        xp1[0] + (xp2[0] - xp1[0]) * line_frac,
        xp1[1] + (xp2[1] - xp1[1]) * line_frac,
    ]

    p2 = [
        xp2[0] - (xp2[0] - xp1[0]) * line_frac,
        xp2[1] - (xp2[1] - xp1[1]) * line_frac,
    ]

    n = np.linspace(0, points, points)
    alpha = np.arctan((p2[1] - p1[1]) / np.array([(p2[0] - p1[0])]))
    w = rot / points * (2 * np.pi)  # + np.pi / points
    ret = (
        p1[0]
        + (p2[0] - p1[0]) * (n / points)
        + amp * np.sin(w * n) * (0 * np.cos((alpha)) - np.sin((alpha))),
        p1[1]
        + (p2[1] - p1[1]) * (n / points)
        + amp * np.sin(w * n) * (0 * np.sin((alpha)) + np.cos((alpha))),
    )

    x, y = (
        np.append(np.insert(ret[0], 0, xp1[0]), xp2[0]),
        np.append(np.insert(ret[1], 0, xp1[1]), xp2[1]),
    )
    plt.plot(x, y, "k-")


def combine_lines(lines):
    return lambda *a, **k: [l(*a, **k) for l in lines]


namedlines = {
    "straight": line,
    "gluon": spring,
    "photon": wave,
    "boson": wave,
    "vector": wave,
    "ghost": dotted,
    "fermion": line,
    "higgs": dashed,
    "gluino": combine_lines([spring, line]),
    "gaugino": combine_lines([wave, line]),
    "phantom": lambda *a, **k: None,
}


class MPLRender(Render):
    def __init__(self, fd=None, *args, **kwargs):
        super().__init__(fd, *args, **kwargs)

    def render(
        self,
        file=None,
        show=True,
        width=None,
        height=None,
        resolution=100,
        clean_up=False,
    ):
        idtopos = {}
        for v in self.fd.vertices:
            idtopos[v.id] = (v.x, v.y)
        for l in self.fd.legs:
            idtopos[l.id] = (l.x, l.y)

        for p in self.fd.propagators:
            namedlines[p.type](idtopos[p.source], idtopos[p.target])
        for l in self.fd.legs:
            if l.sense[:2] == "in":
                namedlines[l.type](idtopos[l.id], idtopos[l.target])
            elif l.sense[:3] == "out":
                namedlines[l.type](idtopos[l.target], idtopos[l.id])
            else:
                raise Exception("Unknown sense")
        plt.axis("off")
        if show:
            plt.show()
        if file is not None:
            plt.savefig(file)
        if clean_up:
            plt.close()

    @staticmethod
    def valid_attribute(attr: str) -> bool:
        return super(MPLRender, MPLRender).valid_attribute(attr) or attr in ["x", "y"]

    @staticmethod
    def valid_type(typ: str) -> bool:
        if typ.lower() in namedlines:
            return True
        return False
