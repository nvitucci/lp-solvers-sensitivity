import pathlib

from math import inf

from sensitivity.glpk import process, Record, Section


class TestGLPK:
    def test_simple(self):
        ranges = process(pathlib.Path(__file__).parent / "files" / "ranges_glpk.txt")

        assert ranges[Section.ROW][0] == Record(
            no=1,
            name="c_e_x50_",
            st="NS",
            activity=45.0,
            slack=0.0,
            obj_coef=None,
            marginal=1.0,
            bounds=(45.0, 45.0),
            activity_range=(45.0, 45.0),
            obj_coef_range=(-inf, inf),
            obj_value_break_range=(10920.0, 10920.0),
            limiting_variables=("c_e_x65_", "c_e_x65_"),
        )
        assert ranges[Section.COL][0] == Record(
            no=1,
            name="x2",
            st="BS",
            activity=45.0,
            slack=None,
            obj_coef=28.0,
            marginal=0.0,
            bounds=(0.0, inf),
            activity_range=(45.0, 37.0),
            obj_coef_range=(-inf, 67.0),
            obj_value_break_range=(-inf, 12675.0),
            limiting_variables=(None, "x14"),
        )
