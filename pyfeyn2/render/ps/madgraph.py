import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List

from IPython.display import display
from wand.image import Image as WImage

from pyfeyn2.render.render import Render

type_map = {
    "line": "Ffermion",
    "plain": "Ffermion",
    "fermion": "Ffermion",
    "higgs": "FHiggs",
    "ghost": "Fghost",
    "photon": "0 Fphoton",
    "gluon": "Fgluon",
    "scurly": ["Fgluon", "Ffermion"],
    "swavy": ["0 Fphoton", "Ffermion"],
    "phantom": "phantom",
}

shape_map = {
    "empty": "empty",
    "blob": "Fblob",
}


def feynman_to_ps(fd):
    text = "%%%%!PS-Adobe-2.0\n"
    text += "%%%%DocumentFonts: Helvetica\n"
    text += "%%%%" + "BoundingBox: -20 -20 %(width)s %(height)s \n"
    # text += "%%%%Pages: 1\n"
    text += "%(header)s"
    text += "/PageWidth 10 def\n"
    text += "/PageHeight 10 def\n"
    text += "/PageSize [PageWidth PageHeight] def\n"

    for p in fd.propagators:
        style = fd.get_style(p)
        src = fd.get_vertex(p.source)
        dst = fd.get_vertex(p.target)
        line = type_map[style.getProperty("line").value]
        if line == "phantom":
            continue
        text += f"{src.x} {src.y} {dst.x} {dst.y} {line} \n"
    for l in fd.legs:
        style = fd.get_style(l)
        dst = fd.get_vertex(l.target)
        line = type_map[style.getProperty("line").value]
        if line == "phantom":
            continue
        if l.is_incoming():
            text += f"{l.x} {l.y} {dst.x} {dst.y} {line} \n"
        elif l.is_outgoing():
            text += f"{dst.x} {dst.y} {l.x} {l.y} {line} \n"
        else:
            raise Exception("Unknown leg sense. Should be either incoming or outgoing.")
    text += "showpage\n"
    text += "%%%%trailer\n"
    return text


class MadGraphRender(Render):
    def __init__(
        self,
        fd=None,
        *args,
        **kwargs,
    ):
        super().__init__(fd)
        if fd is not None:
            self.set_feynman_diagram(fd)

    def render(
        self,
        file=None,
        show=True,
        resolution=100,
        width=100,
        height=100,
        clean_up=True,
        temp_dir=None,
    ):
        if temp_dir is None:
            temp_dir = tempfile.TemporaryDirectory()
        ps = self.get_src() % {"width": width, "height": height, "header": header}
        copy = True
        if file is None:
            copy = False
            file = "tmp"
        file = re.sub(r"\.e?ps$", "", re.sub(r"\.pdf$", "", file.strip()))
        tfile = re.sub(
            r"\.e?ps$", "", re.sub(r"\.pdf$", "", os.path.basename(file).strip())
        )
        tfile = os.path.join(temp_dir.name, tfile)
        with open(tfile + ".ps", "w") as f:
            f.write(ps)
        subprocess.call(
            # ["gs",
            # "-sDEVICE=pdfwrite",
            # "-sOutputFile=" +tfile + ".pdf",
            # "-dBATCH",
            # "-dNOPAUSE",
            #     tfile + ".ps"],
            ["ps2pdf", "-dEPSCrop", f"-g{width*10}x{height*10}", tfile + ".ps"],
            cwd=temp_dir.name,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
        wi = WImage(
            filename=tfile + ".pdf", resolution=resolution, width=width, height=height
        )
        if copy:
            # Copy tfile to file
            Path(file).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(tfile + ".ps", file + ".ps")
            shutil.copy(tfile + ".pdf", file + ".pdf")
        if clean_up and temp_dir:
            temp_dir.cleanup()
        if show:
            display(wi)
        return wi

    def set_feynman_diagram(self, fd):
        super().set_feynman_diagram(fd)
        self.set_src(feynman_to_ps(fd))

    @classmethod
    def valid_styles(cls) -> bool:
        return super().valid_styles() + []

    @classmethod
    def valid_attributes(cls) -> List[str]:
        return super().valid_attributes() + [
            "label",
            "style",
        ]

    @classmethod
    def valid_types(cls) -> List[str]:
        return super().valid_types() + list(type_map.keys())

    @classmethod
    def valid_shapes(cls) -> List[str]:
        return super().valid_types() + list(shape_map.keys())


header = """
%!MadGraph
%
% Feynman Diagrams drawn by MadGraph5_aMC@NLO
%
% Using FEYNMAN DRAW
% A program by David J. Summers to draw
% Feynman diagrams. (c) 1992
% Version 2.7 (c) 1993
%
% Comments and questions to 
%  D.J.Summers@uk.ac.durham
%

/Fnopoints 10 def 
/Fr 2.5 def 
/pi 3.14159265359 def

/Frmod {dup 360 div floor 360 mul sub} def
/Fsign {0 ge {1} {-1} ifelse} def

/Fbasis
{/Fby exch def /Fbx exch def /Fdist Fbx Fbx
mul Fby Fby mul add sqrt def /Fxl Fbx Fdist
div Fr mul def /Fyl Fby Fdist div Fr mul def
/Fxt Fby Fdist div Fr mul def /Fyt Fbx neg
Fdist div Fr mul def } def

/Fstraight 
{/Fshape exch def /Ftype exch def /Fy2 exch
def /Fx2 exch def /Fy1 exch def /Fx1 exch def
Fx2 Fx1 sub Fy2 Fy1 sub Fbasis /Fttype 1
Ftype 2 mod 2 mul abs sub def Ftype 0 ge
{/Fddist Fdist Fr div 2 div def /Fn Fddist round
def Ftype 1 gt {/Fn Fn Fddist Fn sub Fsign
add def} if} {/Fn Fdist Fr div 2 div round 2
mul def} ifelse Fx1 Fy1 moveto 0 1 Fnopoints
Fn mul {/Fi exch def Fshape lineto } for
stroke } def

/Floop
{/Fshape exch def /Fe exch def /Ftype exch
def /Fy2 exch def /Fx2 exch def /Fy1 exch def
/Fx1 exch def /Flam 1 Fe Fe mul sub 2 div Fe
div def /Fxc Fx1 Fx2 Flam Fy2 Fy1 sub mul add
add 2 div def /Fyc Fy1 Fy2 Flam Fx1 Fx2 sub
mul add add 2 div def /Frr Fx1 Fxc sub dup
mul Fy1 Fyc sub dup mul add sqrt def /Fth1
Fy1 Fyc sub Fx1 Fxc sub atan def /Fth2 Fy2
Fyc sub Fx2 Fxc sub atan def Fe 0 lt Fth2
Fth1 lt and {/Fth1 Fth1 360 sub def} if Fe 0
gt Fth2 Fth1 gt and {/Fth2 Fth2 360 sub def}
if /Fdth Fth2 Fth1 sub Fsign def /Fttype 1
Ftype 2 mod abs 2 mul sub def Ftype 0 ge
{/Fddist Fth2 Fth1 sub abs 180 div pi mul Frr
mul Fr div def /Fn Fddist round def Ftype 1
gt {/Fn Fn Fddist Fn sub Fsign add def} if}
{/Fn Fth2 Fth1 sub abs 180 div pi mul Frr mul
Fr div 2 div round 2 mul def} ifelse Fx1 Fy1
moveto 0 1 Fnopoints Fn mul {/Fi exch def
/Fth Fth1 Fth2 Fth1 sub Fi mul Fnopoints div
Fn div add Frmod def Fth sin neg Fdth mul Fth
cos Fdth mul Fbasis Fshape lineto } for
stroke } def

/Farrow
{ moveto Fxt Fxl sub Fyt Fyl sub
rlineto Fxl 2 mul Fxt sub Fyl 2 mul Fyt sub
rlineto Fxl 2 mul Fxt add neg Fyl 2 mul Fyt
add neg rlineto fill } def

/Fphoton
{{ Fx1 Fx2 Fx1 sub Fi mul Fnopoints div Fn
div Fxt Fi 360 mul Fnopoints div Frmod sin
mul Fttype mul 2 div add add Fy1 Fy2 Fy1 sub
Fi mul Fnopoints div Fn div Fyt Fi 360 mul
Fnopoints div Frmod sin mul Fttype mul 2 div
add add } Fstraight } def

/Fphotonr
{{ Fx1 Fx2 Fx1 sub Fi mul Fnopoints div Fn
div Fxt Fi 180 mul Fnopoints div Frmod sin
mul Fttype mul 1 div add add Fy1 Fy2 Fy1 sub
Fi mul Fnopoints div Fn div Fyt Fi 180 mul
Fnopoints div Frmod sin mul Fttype mul 1 div
add add } Fstraight } def

/Fphotond
{{ Fx1 Fx2 Fx1 sub Fi mul Fnopoints div Fn
div Fxt Fi 360 mul Fnopoints div Frmod sin
mul Fttype mul 2 div add add Fy1 Fy2 Fy1 sub
Fi mul Fnopoints div Fn div Fyt Fi 360 mul
Fnopoints div Frmod sin mul Fttype mul 2 div
add add } Fstraight Fx1
Fx2 add 2 div Fy1 Fy2 add 2 div Farrow} def

/Fphotonl
{exch dup 3 1 roll 0 ge {{ Fxc Fth cos Frr
mul Fxt Fi 180 mul Fnopoints div Frmod sin
mul Fttype mul 2 div add add Fyc Fth sin Frr
mul Fyt Fi 180 mul Fnopoints div Frmod sin
mul Fttype mul 2 div add add }} {{ Fxc Fth
cos Frr mul Fxt 1 Fi 180 mul Fnopoints div
Frmod cos sub mul Fttype mul 2 div add add
Fyc Fth sin Frr mul Fyt 1 Fi 180 mul
Fnopoints div Frmod cos sub mul Fttype mul 2
div add add }} ifelse Floop } def

/Fgluon
{2 sub { Fx1 Fx2 Fx1 sub Fi mul Fnopoints div
Fn div Fxt 1 Fi 180 mul Fnopoints div cos sub
mul Fttype mul Fxl Fi 180 mul Fnopoints div
sin mul add add add Fy1 Fy2 Fy1 sub Fi mul
Fnopoints div Fn div Fyt 1 Fi 180 mul
Fnopoints div cos sub mul Fttype mul Fyl Fi
180 mul Fnopoints div sin mul add add add }
Fstraight } def

/Fgluonr
{2 sub { Fx1 Fx2 Fx1 sub Fi mul Fnopoints div
Fn div Fxt 0 Fi 120 mul Fnopoints div cos sub
mul Fttype mul Fxl Fi 120 mul Fnopoints div
sin mul add add add Fy1 Fy2 Fy1 sub Fi mul
Fnopoints div Fn div Fyt 0 Fi 120 mul
Fnopoints div cos sub mul Fttype mul Fyl Fi
120 mul Fnopoints div sin mul add add add }
Fstraight } def


/Fgluonl
{exch 2 sub exch { Fxc Fth cos Frr mul Fxt 1
Fi 180 mul Fnopoints div cos sub mul Fttype
mul Fxl Fi 180 mul Fnopoints div sin mul add
add add Fyc Fth sin Frr mul Fyt 1 Fi 180 mul
Fnopoints div cos sub mul Fttype mul Fyl Fi
180 mul Fnopoints div sin mul add add add }
Floop} def

/Ffermion
{/Fy2 exch def /Fx2 exch def /Fy1 exch def
/Fx1 exch def newpath Fx2 Fx1 sub Fy2 Fy1 sub
Fbasis Fx1 Fy1 moveto Fx2 Fy2 lineto stroke Fx1
Fx2 add 2 div Fy1 Fy2 add 2 div Farrow } def

/Fscalar
{newpath moveto lineto stroke} def

/Ffermionl
{/Fe exch def /Fy2 exch def /Fx2 exch def
/Fy1 exch def /Fx1 exch def newpath /Flam 1 Fe
Fe mul sub 2 div Fe div def /Fxc Fx1 Fx2 Flam Fy2
Fy1 sub mul add add 2 div def /Fyc Fy1 Fy2
Flam Fx1 Fx2 sub mul add add 2 div def /Frr
Fx1 Fxc sub dup mul Fy1 Fyc sub dup mul add
sqrt def /Fth1 Fy1 Fyc sub Fx1 Fxc sub atan
def /Fth2 Fy2 Fyc sub Fx2 Fxc sub atan def Fe
0 lt Fth2 Fth1 lt and {/Fth1 Fth1 360 sub
def} if Fe 0 gt Fth2 Fth1 gt and {/Fth2 Fth2
360 sub def} if /Fthc Fth1 Fth2 add 2 div def
Fxc Fyc Frr Fth1 Fth2 Fe 0 gt {arcn} {arc}
ifelse stroke Fthc sin Fe 0 lt {neg} if Fthc
cos Fe 0 gt {neg} if Fbasis Fxc Fthc cos Frr
mul add Fyc Fthc sin Frr mul add Farrow } def

/Fscalarl
{/Fe exch def /Fy2 exch def /Fx2 exch def
/Fy1 exch def /Fx1 exch def newpath /Flam 1 Fe
Fe mul sub 2 div Fe div def /Fxc Fx1 Fx2 Flam Fy2
Fy1 sub mul add add 2 div def /Fyc Fy1 Fy2
Flam Fx1 Fx2 sub mul add add 2 div def /Frr
Fx1 Fxc sub dup mul Fy1 Fyc sub dup mul add
sqrt def /Fth1 Fy1 Fyc sub Fx1 Fxc sub atan
def /Fth2 Fy2 Fyc sub Fx2 Fxc sub atan def Fe
0 lt Fth2 Fth1 lt and {/Fth1 Fth1 360 sub
def} if Fe 0 gt Fth2 Fth1 gt and {/Fth2 Fth2
360 sub def} if /Fthc Fth1 Fth2 add 2 div def
Fxc Fyc Frr Fth1 Fth2 Fe 0 gt {arcn} {arc}
ifelse stroke } def

/Fblob 
{/Fshade exch def newpath Fr mul 0 360 arc gsave
1 Fshade sub setgray fill grestore stroke} def

/Fhiggs
{/Fy2 exch def /Fx2 exch def /Fy1 exch def
/Fx1 exch def gsave Fx1 Fx2 sub dup mul
Fy1 Fy2 sub dup mul add sqrt dup Fr div
2 div round 2 mul 1 add div /dashln exch def
[dashln dashln] 0 setdash Fx1 Fy1 moveto
Fx2 Fy2 lineto stroke grestore} def


/Fhiggsd
{/Fy2 exch def /Fx2 exch def /Fy1 exch def
/Fx1 exch def gsave Fx1 Fx2 sub dup mul
Fy1 Fy2 sub dup mul add sqrt dup Fr div
2 div round 2 mul 1 add div /dashln exch def
[dashln dashln] 0 setdash Fx1 Fy1 moveto
Fx2 Fy2 lineto stroke grestore Fx1 Fx2 add 2 div
Fy1 Fy2 add 2 div Farrow} def

/Fhiggsl
{/Fe exch def /Fy2 exch def /Fx2 exch def
/Fy1 exch def /Fx1 exch def /Flam gsave 1 Fe
Fe mul sub 2 div Fe div def /Fxc Fx1 Fx2 Flam
Fy2 Fy1 sub mul add add 2 div def /Fyc Fy1
Fy2 Flam Fx1 Fx2 sub mul add add 2 div def
/Frr Fx1 Fxc sub dup mul Fy1 Fyc sub dup mul
add sqrt def /Fth1 Fy1 Fyc sub Fx1 Fxc sub
atan def /Fth2 Fy2 Fyc sub Fx2 Fxc sub atan
def Fe 0 lt Fth2 Fth1 lt and {/Fth1 Fth1 360
sub def} if Fe 0 gt Fth2 Fth1 gt and {/Fth2
Fth2 360 sub def} if /Fthc Fth1 Fth2 add 2
div def Fxc Fyc Frr Fth1 Fth2 Fe 0 gt {arcn}
{arc} ifelse Fth2 Fth1 sub abs 180 div pi mul
Frr mul dup Fr div 2 div round 2 mul 1 add
div /dashln exch def [dashln dashln] 0
setdash stroke grestore} def

/Fghost
{/Fy2 exch def /Fx2 exch def /Fy1 exch def
/Fx1 exch def Fx2 Fx1 sub Fy2 Fy1 sub Fbasis
/Fn Fx1 Fx2 sub dup mul Fy1 Fy2 sub dup mul
add sqrt Fr div round def 0 1 Fn {/Fi exch
def Fx2 Fx1 sub Fi Fn div mul Fx1 add Fy2 Fy1
sub Fi Fn div mul Fy1 add Fr 10 div 0 360 arc
fill} for Fx1 Fx2 add 2 div Fy1 Fy2 add 2 div
Farrow } def

/Fghostl
{/Fe exch def /Fy2 exch def /Fx2 exch def
/Fy1 exch def /Fx1 exch def /Flam 1 Fe Fe mul
sub 2 div Fe div def /Fxc Fx1 Fx2 Flam Fy2
Fy1 sub mul add add 2 div def /Fyc Fy1 Fy2
Flam Fx1 Fx2 sub mul add add 2 div def /Frr
Fx1 Fxc sub dup mul Fy1 Fyc sub dup mul add
sqrt def /Fth1 Fy1 Fyc sub Fx1 Fxc sub atan
def /Fth2 Fy2 Fyc sub Fx2 Fxc sub atan def Fe
0 lt Fth2 Fth1 lt and {/Fth1 Fth1 360 sub
def} if Fe 0 gt Fth2 Fth1 gt and {/Fth2 Fth2
360 sub def} if /Fthc Fth1 Fth2 add 2 div def
/Fn Fth2 Fth1 sub abs 180 div pi mul Frr mul
Fr div round def 0 1 Fn {/Fi exch def Fth2
Fth1 sub Fi Fn div mul Fth1 add dup cos Frr
mul Fxc add exch sin Frr mul Fyc add Fr 10
div 0 360 arc fill} for Fthc sin Fe 0 lt
{neg} if Fthc cos Fe 0 gt {neg} if Fbasis Fxc
Fthc cos Frr mul add Fyc Fthc sin Frr mul add
Farrow } def

/Fproton
{/Fy2 exch def /Fx2 exch def /Fy1 exch def
/Fx1 exch def Fx2 Fx1 sub Fy2 Fy1 sub Fbasis
Fx1 Fxt 2 div add Fy1 Fyt 2 div add moveto
Fx2 Fxt 2 div add Fy2 Fyt 2 div add lineto
Fx1 Fxt 2 div sub Fy1 Fyt 2 div sub moveto
Fx2 Fxt 2 div sub Fy2 Fyt 2 div sub lineto
Fx1 Fx2 add 2 div Fxt Fxl sub add Fy1 Fy2 add
2 div Fyt Fyl sub add moveto Fx1 Fx2 add Fxl
add 2 div Fy1 Fy2 add Fyl add 2 div lineto
Fx1 Fx2 add 2 div Fxt Fxl add sub Fy1 Fy2 add
2 div Fyt Fyl add sub lineto stroke} def

/Fmax {2 copy lt {exch} if pop} def
/Fstart {gsave currentpoint
translate 0 0 moveto 0 rm Fr 4 mul
scalefont setfont} def
/Fsubspt {gsave currentpoint Fcharheight 5 div
sub translate 0.6 0.6 scale 0 0 moveto 0} def
/Fsupspt {gsave currentpoint Fcharheight 0.6 mul
add translate 0.6 0.6 scale 0 0 moveto 0} def
/Feend {currentpoint pop Fmax 0.6 mul
grestore currentpoint pop add Fmax} def
/Fendd {pop grestore} def
/Fshow {exch 0 moveto show currentpoint pop} def
/Fcharheight
{gsave (X) true charpath flattenpath pathbbox
3 1 roll pop sub exch pop grestore} def

/Foverline
{exch 0 moveto gsave dup true charpath
flattenpath pathbbox Fcharheight 10 div dup
2 div setlinewidth add dup 4
1 roll newpath moveto pop lineto stroke
grestore show currentpoint pop} def

/Funderline 
{exch 0 moveto gsave dup true charpath
flattenpath pathbbox pop exch Fcharheight
10 div dup 2 div setlinewidth
sub dup 3 1 roll newpath moveto lineto stroke
grestore show currentpoint pop} def

/rm /Times-Roman findfont def
/it /Times-Italic findfont def
/sy /Symbol findfont def

/wedge 
/{ /ystop exch def /xstop exch def /ystart exch def
/xstart exch def /delx xstop xstart sub def /dely 
ystop ystart sub def /dist delx dup mul dely dup 
mul add sqrt def /halfdist dist 2 div def
/angle dely delx atan def xstart ystart moveto 
angle rotate 0 halfdist rlineto dist halfdist
neg rlineto dist neg halfdist neg rlineto 
0 halfdist rlineto }def

/ch_photon
{/ystop exch def /xstop exch def /ystart exch def
/xstart exch def /xmid xstart xstop add 2 div def
/ymid ystart ystop add 2 div def
/dx xstop xstart sub def /dy ystop ystart sub def
/length dx dup mul dy dup mul add sqrt def
/xunit dx length div def /yunit dy length div def
/x1 xmid xunit -4.8 mul add def
/y1 ymid yunit -4.8 mul add def
/x2 xmid xunit 4.8 mul add def
/y2 ymid yunit 4.8 mul add def
/y2 ymid yunit 4.8 mul add def
xstart ystart x1 y1 1 Fphoton 
x2 y2 xstop ystop 1 Fphoton
/x1 xmid xunit -5.2 mul add def 
/y1 ymid yunit -5.2 mul add def
/x2 xmid xunit 5.2 mul add def 
/y2 ymid yunit 5.2 mul add def
gsave x1 y1 x2 y2 wedge fill grestore} def

/ch_higgs 
{ /ystop exch def /xstop exch def /ystart exch def
/xstart exch def 
/xmid xstart xstop add 2 div def
/ymid ystart ystop add 2 div def
/dx xstop xstart sub def /dy ystop ystart sub def
/length dx dup mul dy dup mul add sqrt def
/xunit dx length div def /yunit dy length div def
/x1 xmid xunit -4.8 mul add def 
/y1 ymid yunit -4.8 mul add def
/x2 xmid xunit 4.8 mul add def 
/y2 ymid yunit 4.8 mul add def
xstart ystart x1 y1 Fhiggs 
x2 y2 xstop ystop Fhiggs
/x1 xmid xunit -5.2 mul add def
/y1 ymid yunit -5.2 mul add def
/x2 xmid xunit 5.2 mul add def
/y2 ymid yunit 5.2 mul add def
gsave x1 y1 x2 y2 wedge fill grestore} def
%% End of the header

%%Page:       1       1
%%PageBoundingBox:-20 -20 %(width)s %(height)s
%%PageFonts: Helvetica
"""
