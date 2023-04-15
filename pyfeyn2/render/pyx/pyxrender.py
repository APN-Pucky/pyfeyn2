import os
from warnings import warn

import pyx
from IPython.display import display
from pyx import *
from wand.image import Image as WImage

# from pyfeyn2.feynmandiagram import Line, Point
from pyfeyn2.render.pyx.deco import Arrow, PointLabel
from pyfeyn2.render.pyx.diagrams import FeynDiagram
from pyfeyn2.render.pyx.lines import Line, NamedLine
from pyfeyn2.render.pyx.points import SQUARE, DecoratedPoint, NamedMark, Point
from pyfeyn2.render.render import Render


class PyxRender(Render):
    def __init__(self, fd=None, *args, **kwargs):
        super().__init__(fd, *args, **kwargs)

    def render(
        self,
        file=None,
        show=True,
        resolution=200,
        width=None,
        height=None,
        clean_up=False,
    ):
        delete = False
        if file is None:
            file = "tmp.pdf"
            delete = True
        pyxfd = FeynDiagram()
        for v in self.fd.vertices:
            dp = DecoratedPoint(v.x, v.y)
            dp = self.apply_layout(self.fd.get_style(v).cssText.replace("\n", " "), dp)
            if v.label is not None:
                dp.setFillstyles(PointLabel(dp, v.label, displace=3, angle=90))
            pyxfd.add(dp)
        for l in self.fd.legs:
            lstyle = self.fd.get_style(l)
            tar = self.fd.get_vertex(l.target)
            if lstyle.getProperty("line") is not None:
                lname = lstyle.getProperty("line").value
            else:
                lname = l.type  # fallback to type
            if l.is_incoming():
                nl = NamedLine[lname](Point(l.x, l.y), Point(tar.x, tar.y))
            elif l.is_outgoing():
                nl = NamedLine[lname](Point(tar.x, tar.y), Point(l.x, l.y))
            if lstyle.getProperty("bend") is not None:
                nl = nl.bend(lstyle.getProperty("bend").value)
            nl = self.apply_layout(self.fd.get_style(l).cssText.replace("\n", " "), nl)
            nl = nl.addLabel(l.label)

        for p in self.fd.propagators:
            pstyle = self.fd.get_style(p)
            src = self.fd.get_vertex(p.source)
            tar = self.fd.get_vertex(p.target)
            if pstyle.getProperty("line") is not None:
                lname = pstyle.getProperty("line").value
            else:
                lname = p.type
            nl = NamedLine[lname](Point(src.x, src.y), Point(tar.x, tar.y))
            if pstyle.getProperty("bend") is not None:
                nl = nl.bend(pstyle.getProperty("bend").value)
            nl = self.apply_layout(self.fd.get_style(p).cssText.replace("\n", " "), nl)
            nl = nl.addLabel(p.label)
        pyxfd.draw(file)
        # print("Drawing to %s" % file)
        wi = WImage(filename=file, resolution=resolution, width=width, height=height)
        if delete:
            os.remove(file)
        if show:
            display(wi)
        if clean_up:
            # TODO: clean up
            pass
        return wi

    def apply_layout(self, stylestring, obj):
        """Apply the decorators encoded in a style string to an object."""
        if stylestring is None:
            return obj
        styleelements = stylestring.split(";")
        styledict = {}
        for styling in styleelements:
            if styling == "":
                break
            s = styling.split(":")
            styledict[s[0].lstrip().rstrip()] = s[1]
        if "fill-style" in styledict:
            filltype = styledict["fill-style"].split()
            if filltype[0] == "solid":
                R, G, B = [
                    int("0x" + x, base=16) / 255.0
                    # eval("0x%s" % x) / 255.0 # <- old code
                    for x in [filltype[1][n : n + 2] for n in (1, 3, 5)]
                ]
                obj.fillstyles = [pyx.color.rgb(R, G, B)]
            elif filltype[0] == "hatched":
                D, A = float(filltype[1]), int(filltype[2])
                obj.fillstyles = [pyx.pattern.hatched(D, A)]
            elif filltype[0] == "crosshatched":
                D, A = float(filltype[1]), int(filltype[2])
                obj.fillstyles = [pyx.pattern.crosshatched(D, A)]
        if ("mark-shape" in styledict or "mark-size" in styledict) and isinstance(
            obj, DecoratedPoint
        ):
            try:
                marktype = NamedMark[styledict["mark-shape"]]
            except Exception:
                marktype = SQUARE
            try:
                marksize = float(styledict["mark-size"])
            except Exception:
                marksize = 0.075
            obj.setMark(marktype(size=marksize))
        if (
            "arrow-size" in styledict
            or "arrow-angle" in styledict
            or "arrow-constrict" in styledict
            or "arrow-pos" in styledict
            or "arrow-sense" in styledict
            or "arrow-displace" in styledict
        ) and isinstance(obj, Line):
            try:
                arrsize = pyx.unit.length(float(styledict["arrow-size"]), unit="cm")
            except Exception:
                arrsize = 6 * pyx.unit.v_pt
            try:
                arrangle = float(styledict["arrow-angle"])
            except Exception:
                arrangle = 45
            try:
                arrconstrict = float(styledict["arrow-constrict"])
            except Exception:
                arrconstrict = 0.8
            try:
                arrpos = float(styledict["arrow-pos"])
            except Exception:
                arrpos = 0.5
            try:
                arrsense = float(styledict["arrow-sense"])
            except Exception:
                arrsense = 1
            if arrsense == 1 or arrsense == -1:
                obj.addArrow(
                    arrow=Arrow(arrpos, arrsize, arrangle, arrconstrict, arrsense)
                )
            elif arrsense == 0:
                # no arrow
                pass
            else:
                warn("arrow-sense must be 1, -1 or 0 (no arrow).")
            # obj.addArrow(arrow=Arrow(arrpos, arrsize, arrangle, arrconstrict, arrsense))
        if (
            "momentum-arrow" in styledict
            or "momentum-arrow-sense" in styledict
            or "parallel-arrow-size" in styledict
            or "parallel-arrow-angle" in styledict
            or "parallel-arrow-constrict" in styledict
            or "parallel-arrow-pos" in styledict
            or "parallel-arrow-length" in styledict
            or "parallel-arrow-displace" in styledict
            or "parallel-arrow-sense" in styledict
        ) and isinstance(obj, Line):
            try:
                arrsize = pyx.unit.length(
                    float(styledict["parallel-arrow-size"]), unit="cm"
                )
            except Exception:
                arrsize = 6 * pyx.unit.v_pt
            try:
                arrangle = float(styledict["parallel-arrow-angle"])
            except Exception:
                arrangle = 45
            try:
                arrconstrict = float(styledict["parallel-arrow-constrict"])
            except Exception:
                arrconstrict = 0.8
            try:
                arrpos = float(styledict["parallel-arrow-pos"])
            except Exception:
                arrpos = 0.5
            try:
                arrlen = float(styledict["parallel-arrow-length"])
            except Exception:
                arrlen = 0.5 * pyx.unit.v_cm
            try:
                arrdisp = float(styledict["parallel-arrow-displace"])
            except Exception:
                arrdisp = 0.3
            try:
                arrsense = int(styledict["momentum-arrow-sense"])
            except Exception:
                arrsense = +1
                try:
                    arrsense = int(styledict["parallel-arrow-sense"])
                except Exception:
                    arrsense = +1
            if arrsense == 1 or arrsense == -1:
                obj.addParallelArrow(
                    arrpos, arrdisp, arrlen, arrsize, arrangle, arrconstrict, arrsense
                )
            elif arrsense == 0:
                # no arrow
                pass
            else:
                warn("momentum-arrow-sense must be 1, -1 or 0 (no arrow).")
        if "is3d" in styledict and isinstance(obj, Line):
            fwords = ["0", "no", "false", "f", "off"]
            twords = ["1", "yes", "true", "t", "on"]
            if styledict["is3d"].lstrip().lower() in fwords:
                obj.set3D(False)
            elif styledict["is3d"].lstrip().lower() in twords:
                obj.set3D(True)
        return obj

    @classmethod
    def valid_types(cls):
        return super(PyxRender, cls).valid_types() + list(NamedLine.keys())

    @classmethod
    def valid_attributes(cls):
        return super(PyxRender, cls).valid_attributes() + [
            "style",
            "type",
            "label",
            "x",
            "y",
        ]

    @classmethod
    def valid_styles(cls):
        return super(PyxRender, cls).valid_styles() + [
            "line",
            "bend",
            "arrow-pos",
            "arrow-sense",
            "arrow-size",
            "arrow-angle",
            "arrow-constrict",
        ]
