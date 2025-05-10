# Adapted code from https://github.com/aminnj/pyfeyn/blob/main/pyfeyn.py
import math

import ROOT as r

color_map = {
    None: None,
    "": r.kBlack,
    "white": r.kWhite,
    "black": r.kBlack,
    "red": r.kRed,
    "green": r.kGreen,
    "blue": r.kBlue,
    "cyan": r.kCyan,
    "magenta": r.kMagenta,
    "yellow": r.kYellow,
    "gray": r.kGray,
    "orange": r.kOrange,
    "pink": r.kPink,
    "purple": r.kViolet,
    "brown": r.kBrown,
}


class Label(object):
    def __init__(
        self,
        text="",
        x1=0.0,
        y1=0.0,
        offsetx=0,
        offsety=0,
        textsize=0.08,
        textalign=22,
        roman=False,
    ):
        self.x1 = x1
        self.y1 = y1
        if text is not None:
            self.text = text.replace("$", "")
        else:
            self.text = None
        self.offsetx = offsetx
        self.offsety = offsety
        self.textsize = textsize
        self.textalign = textalign
        self.roman = roman

    def set_location(self, x, y):
        self.x1 = x
        self.y1 = y

    def transform_text(self, text):
        # ROOT needs one of these characters to put in a $ and go into mathmode
        # otherwise we do it explicitly
        if self.roman or any([x in text for x in "#{}^"]):
            return text
        text = "${0}$".format(text)
        return text

    def draw(self):

        if not self.text:
            return
        t = r.TLatex()
        t.SetTextAlign(self.textalign)
        t.SetTextSize(self.textsize)
        t.DrawLatex(
            self.x1 + self.offsetx,
            self.y1 + self.offsety,
            self.text,
            # self.transform_text(self.text),
        )


class Marker(object):
    def __init__(self, color=None, radius=2, linewidth=0):
        self.x = None
        self.y = None
        self.color = color_map[color]
        self.radius = radius
        self.linewidth = linewidth

    def set_location(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        if self.color is None:
            return
        m = r.TEllipse(self.x, self.y, self.radius)
        m.SetFillColor(self.color)
        m.SetLineWidth(self.linewidth)
        m.Draw()


class Vertex(object):
    def __init__(self, x1, y1, label=Label(), marker=Marker(), autolabel=True):
        self.x1 = x1
        self.y1 = y1
        self.label = label
        self.marker = marker

        self.marker.set_location(x1, y1)

        if autolabel:
            self.label.set_location(self.x1, self.y1)

    def draw(self, _nodelete=[]):
        self.label.draw()
        self.marker.draw()


class Propagator(object):
    def __init__(
        self,
        v1,
        v2,
        typ="line",
        label=Label(),
        autolabel=True,
        linewidth=2,
        linecolor="black",
        label_shift_amount=0.5,
        double_distance=3,
        # fliparrow=False,
        # noarrow=True,
    ):
        linecolor = color_map[linecolor]
        if linecolor is None:
            linecolor = r.kBlack
        self.double_distance = double_distance
        self.v1 = v1
        self.v2 = v2
        self.typ = typ
        self.label = label
        self.linewidth = linewidth
        self.linecolor = linecolor
        self.fliparrow = False
        self.noarrow = True

        if typ == "fermion":
            self.fliparrow = True
            self.noarrow = False
        if typ == "anti fermion":
            self.fliparrow = False
            self.noarrow = False
        if typ == "baryon":
            self.fliparrow = True
            self.noarrow = False
        if typ == "anti baryon":
            self.fliparrow = False
            self.noarrow = False
        if typ == "squark":
            self.fliparrow = True
            self.noarrow = False
        if typ == "anti squark":
            self.fliparrow = False
            self.noarrow = False

        # Calculate the direction vector
        dx = self.v2.x1 - self.v1.x1
        dy = self.v2.y1 - self.v1.y1

        # Calculate the length of the direction vector
        length = math.sqrt(dx**2 + dy**2)

        # Normalize the orthogonal vector (dy, -dx) or (-dy, dx)
        # Let's use (dy, -dx) for this example
        self.orthogonal_x = dy / length * 2  # * len(self.label.text)
        self.orthogonal_y = -dx / length

        if autolabel and self.label.text is not None:
            # Define the shift amount
            self.label.set_location(
                0.5 * (self.v1.x1 + self.v2.x1)
                + label_shift_amount * self.orthogonal_x,
                0.5 * (self.v1.y1 + self.v2.y1) + label_shift_amount * self.orthogonal_y
                # 0.5 * (self.v1.x1 + self.v2.x1), 0.5 * (self.v1.y1 + self.v2.y1)
            )

    def draw(self, _nodelete=[]):
        prop1, prop2 = None, None
        drawopt = ""
        if self.typ == "line" or self.typ == "fermion" or self.typ == "anti fermion":
            prop1 = r.TLine(self.v1.x1, self.v1.y1, self.v2.x1, self.v2.y1)
        elif self.typ == "baryon" or self.typ == "anti baryon":
            scale = 0.02
            prop1 = r.TLine(
                self.v1.x1 + scale * self.double_distance * self.orthogonal_x,
                self.v1.y1 + scale * self.double_distance * self.orthogonal_y,
                self.v2.x1 + scale * self.double_distance * self.orthogonal_x,
                self.v2.y1 + scale * self.double_distance * self.orthogonal_y,
            )
            prop1.SetLineColor(self.linecolor)
            prop1.SetLineWidth(self.linewidth)
            prop1.Draw(drawopt)
            _nodelete.append(prop1)
            prop1 = r.TLine(
                self.v1.x1 - scale * self.double_distance * self.orthogonal_x,
                self.v1.y1 - scale * self.double_distance * self.orthogonal_y,
                self.v2.x1 - scale * self.double_distance * self.orthogonal_x,
                self.v2.y1 - scale * self.double_distance * self.orthogonal_y,
            )
            prop1.SetLineColor(self.linecolor)
            prop1.SetLineWidth(self.linewidth)
            prop1.Draw(drawopt)
            _nodelete.append(prop1)
            prop1 = r.TLine(self.v1.x1, self.v1.y1, self.v2.x1, self.v2.y1)
        elif self.typ == "phantom":
            pass  # no TLine here, but Vertices are to be drawn later
        elif self.typ == "higgs" or self.typ == "squark" or self.typ == "anti squark":
            prop1 = r.TLine(self.v1.x1, self.v1.y1, self.v2.x1, self.v2.y1)
            r.gStyle.SetLineStyleString(11, "50 30")
            prop1.SetLineStyle(11)
        elif self.typ == "ghost":
            prop1 = r.TLine(self.v1.x1, self.v1.y1, self.v2.x1, self.v2.y1)
            r.gStyle.SetLineStyleString(11, "20 50")
            prop1.SetLineStyle(11)
        elif self.typ == "gluon":
            prop1 = r.TCurlyLine(self.v1.x1, self.v1.y1, self.v2.x1, self.v2.y1)
            prop1.SetWaveLength(prop1.GetWaveLength() * 1.6)
            prop1.SetAmplitude(prop1.GetAmplitude() * 1.4)
        elif self.typ == "photon" or self.typ == "boson":
            prop1 = r.TCurlyLine(self.v1.x1, self.v1.y1, self.v2.x1, self.v2.y1)
            prop1.SetWavy()
            prop1.SetWaveLength(prop1.GetWaveLength() * 1.6)
            prop1.SetAmplitude(prop1.GetAmplitude() * 1.4)
        elif self.typ == "gluino":
            prop1 = r.TCurlyLine(self.v1.x1, self.v1.y1, self.v2.x1, self.v2.y1)
            prop1.SetWavy()
            prop1.SetWaveLength(prop1.GetWaveLength() * 1.6)
            prop1.SetAmplitude(prop1.GetAmplitude() * 1.4)
            prop2 = r.TLine(self.v1.x1, self.v1.y1, self.v2.x1, self.v2.y1)
        elif self.typ == "charged boson":
            prop1 = r.TCurlyLine(self.v1.x1, self.v1.y1, self.v2.x1, self.v2.y1)
            prop1.SetWaveLength(prop1.GetWaveLength() * 1.6)
            prop1.SetAmplitude(prop1.GetAmplitude() * 1.4)
            prop2 = r.TLine(self.v1.x1, self.v1.y1, self.v2.x1, self.v2.y1)
        elif self.typ.startswith("wavyarc"):
            # wavyarc(180,0) -> phimin = 180, phimax = 0
            phimin, phimax = list(
                map(float, self.typ.split("(", 1)[1].split(")", 1)[0].split(","))
            )
            xc = 0.5 * (self.v1.x1 + self.v2.x1)
            yc = 0.5 * (self.v1.y1 + self.v2.y1)
            radius = 0.5 * (self.v2.x1 - self.v1.x1)
            prop1 = r.TCurlyArc(xc, yc, radius, phimin, phimax)
            prop1.SetWavy()
            prop1.SetWaveLength(prop1.GetWaveLength() * 1.6)
            prop1.SetAmplitude(prop1.GetAmplitude() * 1.4)
            prop1.SetFillColorAlpha(0, 0.0)
            drawopt = "only"
        elif self.typ.startswith("arc"):
            # arc(180,0) -> phimin = 180, phimax = 0
            phimin, phimax = list(
                map(float, self.typ.split("(", 1)[1].split(")", 1)[0].split(","))
            )
            xc = 0.5 * (self.v1.x1 + self.v2.x1)
            yc = 0.5 * (self.v1.y1 + self.v2.y1)
            radius = 0.5 * (self.v2.x1 - self.v1.x1)
            prop1 = r.TArc(xc, yc, radius, phimin, phimax)
            prop1.SetFillColorAlpha(0, 0.0)
            drawopt = "only"

        if prop1:
            prop1.SetLineColor(self.linecolor)
            prop1.SetLineWidth(self.linewidth)
            prop1.Draw(drawopt)
            _nodelete.append(prop1)
        if prop2:
            prop2.SetLineColor(self.linecolor)
            prop2.SetLineWidth(self.linewidth)
            prop2.Draw(drawopt)
            _nodelete.append(prop2)

        if not self.noarrow:
            if self.typ.startswith("arc"):
                phimin, phimax = list(
                    map(float, self.typ.split("(", 1)[1].split(")", 1)[0].split(","))
                )
                phi = (0.5 * (phimax - phimin) % 360) * math.pi / 180
                radius = 0.5 * (self.v2.x1 - self.v1.x1)
                xc = 0.5 * (self.v1.x1 + self.v2.x1) + radius * math.cos(phi)
                yc = 0.5 * (self.v1.y1 + self.v2.y1) + radius * math.sin(phi)
                dx, dy = -radius * 0.2 * math.sin(phi), -radius * 0.2 * math.cos(phi)
                if self.fliparrow:
                    dx, dy = -dx, -dy
                awidth = 0.025
                a1 = r.TArrow(
                    xc - dx / 2, yc - dy / 2, xc + dx / 2, yc + dy / 2, awidth, "|>"
                )
                a1.SetLineWidth(0)
                a1.SetFillColor(self.linecolor)
                a1.SetAngle(40)
                a1.Draw()
                _nodelete.append(a1)
            else:
                c1 = self.v1.x1, self.v1.y1
                c2 = self.v2.x1, self.v2.y1
                if self.fliparrow:
                    c1, c2 = c2, c1
                mult = 0.54
                awidth = 0.025
                a1 = r.TArrow(
                    c1[0],
                    c1[1],
                    (1.0 - mult) * c1[0] + mult * c2[0],
                    (1.0 - mult) * c1[1] + mult * c2[1],
                    awidth,
                    "|>",
                )
                a1.SetLineWidth(0)
                a1.SetFillColor(self.linecolor)
                a1.SetAngle(40)
                a1.Draw()
                _nodelete.append(a1)

        self.v1.draw()
        self.v2.draw()
        self.label.draw()
