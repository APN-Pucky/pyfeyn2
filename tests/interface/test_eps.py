from pyfeyn2.interface.eps import eps_to_feynml


def test_load_eps():
    fml = eps_to_feynml("tests/interface/lo.ps")
    assert fml != None
