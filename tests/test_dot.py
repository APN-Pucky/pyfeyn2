from pyfeyn2.render.latex.dot import DotRender, feynman_to_dot
from tests.test_feynman import get_test_gluons, get_test_many_gluons


def test_dot():
    fd = get_test_gluons()

    print(feynman_to_dot(fd))
    dr = DotRender(fd)
    print(dr.get_src())
    dr.render("test.pdf")


def test_dot2():
    fd = get_test_many_gluons()

    print(feynman_to_dot(fd))
    dr = DotRender(fd)
    print(dr.get_src())
    dr.render("test.pdf")


test_dot()
test_dot2()
