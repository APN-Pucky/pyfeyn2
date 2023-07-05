from pyfeyn2.auto.position import feynman_adjust_points
from pyfeyn2.render.text.ascii import ASCIIRender
from pyfeyn2.render.text.unicode import UnicodeRender
from tests.test_feynman import get_test_many_gluons


def test_ascii():
    fd = get_test_many_gluons()
    fd = feynman_adjust_points(fd, clear_vertices=True)

    tfd = ASCIIRender(fd)
    tfd.render()
    print(tfd.get_src_txt())


def test_unicode():
    fd = get_test_many_gluons()
    fd = feynman_adjust_points(fd, clear_vertices=True)

    tfd = UnicodeRender(fd)
    tfd.render()
    print(tfd.get_src_txt())


test_ascii()
test_unicode()
