import pathlib

from math import inf

from sensitivity.cbc import process, Record


class TestGLPK:
    def test_simple(self):
        objective = process(pathlib.Path(__file__).parent / "files" / "obj_cbc.txt")
        rhs = process(pathlib.Path(__file__).parent / "files" / "rhs_cbc.txt")

        assert objective[0] == Record(
            ranging=0, name="x2", increase=39.0000001, inc_variable="x14", decrease=inf, dec_variable=None
        )
        assert rhs[0] == Record(
            ranging=0, name="c_e_x50_", increase=0.0, inc_variable="c_e_x53_", decrease=0.0, dec_variable="c_e_x53_"
        )
