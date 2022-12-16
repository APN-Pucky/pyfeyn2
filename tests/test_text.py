from pyfeyn2.render.latex.dot import feynman_adjust_points
from pyfeyn2.render.text.ascii import ASCIIRender
from pyfeyn2.render.text.unicode import UnicodeRender
from tests.test_feynman import test_many_gluons


def test_ascii():
    fd = test_many_gluons()
    fd = feynman_adjust_points(fd)

    tfd = ASCIIRender(fd)
    tfd.render()
    print(tfd.get_src_txt())


def test_unicode():
    fd = test_many_gluons()
    fd = feynman_adjust_points(fd)

    tfd = UnicodeRender(fd)
    tfd.render()
    print(tfd.get_src_txt())


test_ascii()
test_unicode()