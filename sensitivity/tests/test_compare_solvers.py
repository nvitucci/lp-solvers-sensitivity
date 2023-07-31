import pathlib

from math import isclose

from sensitivity import cbc, glpk


class TestSolvers:
    def test_compare_cols(self):
        glpk_ranges = glpk.process(pathlib.Path(__file__).parent / "files" / "ranges_glpk.txt")
        cbc_objective = cbc.process(pathlib.Path(__file__).parent / "files" / "obj_cbc.txt")

        assert len(glpk_ranges[glpk.Section.COL]) == len(cbc_objective)

        for i in range(len(cbc_objective)):
            glpk_col = glpk_ranges[glpk.Section.COL][i]
            cbc_obj = cbc_objective[i]

            assert glpk_col.name == cbc_obj.name
            assert isclose(-glpk_col.obj_coef_range[0] + glpk_col.obj_coef, cbc_obj.decrease, abs_tol=1e-06)
            assert isclose(glpk_col.obj_coef_range[1] - glpk_col.obj_coef, cbc_obj.increase, abs_tol=1e-06)

            # Not all limiting variables match
            # assert glpk_col.limiting_variables == (cbc_obj.dec_variable, cbc_obj.inc_variable)

    def test_compare_rows(self):
        glpk_ranges = glpk.process(pathlib.Path(__file__).parent / "files" / "ranges_glpk.txt")
        cbc_rhs = cbc.process(pathlib.Path(__file__).parent / "files" / "rhs_cbc.txt")

        assert len(glpk_ranges[glpk.Section.ROW]) == len(cbc_rhs)

        for i in range(len(cbc_rhs)):
            glpk_col = glpk_ranges[glpk.Section.ROW][i]
            cbc_obj = cbc_rhs[i]

            assert glpk_col.name == cbc_obj.name
            assert isclose(-glpk_col.activity_range[0] + glpk_col.activity, cbc_obj.decrease, abs_tol=1e-06)
            assert isclose(glpk_col.activity_range[1] - glpk_col.activity, cbc_obj.increase, abs_tol=1e-06)

            # Not all limiting variables match
            # assert glpk_col.limiting_variables == (cbc_obj.dec_variable, cbc_obj.inc_variable)
