from pyfeyn2.auto.position import feynman_adjust_points
from pyfeyn2.render.latex.tikzfeynman import TikzFeynmanRender
from tests.test_feynman import get_test_gluons, get_test_many_gluons


def test_tikz():
    fd = get_test_gluons()

    tfd = TikzFeynmanRender(fd)
    print(tfd.get_src())
    tfd.render("test.pdf")


def test_dot_positions():
    fd = get_test_many_gluons()
    fd = feynman_adjust_points(fd, clear_vertices=True)

    tfd = TikzFeynmanRender(fd)
    print(tfd.get_src())
    tfd.render("test.pdf")


test_tikz()
test_dot_positions()
