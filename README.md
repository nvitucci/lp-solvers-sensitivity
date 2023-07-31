# lp-solvers-sensitivity

Tools for sensitivity analysis with LP solvers.

Use the `glpk` and `cbc` modules in the `sensitivity` package to convert sensitivity reports to Python objects.
See the tests for examples.

## Notes

As of now, this project is not meant to be a polished, PyPI-ready Python package, but rather a collection of useful classes and code snippets. 
(It may become one in the future, though.)
As such, the project structure is not optimal.

The structure of the Python classes is also subject to change.
Any suggestions are welcome.

## Recreating the test files

### Problem file (from Pyomo model)

The Pyomo model in the [pyomo_script.py](sensitivity/tests/pyomo_script.py) file is based on the Pyomo Cookbook [Transportation Networks example](https://jckantor.github.io/ND-Pyomo-Cookbook/notebooks/03.01-Transportation-Networks.html),
with data from the book _Ricerca operativa. Problemi di gestione della produzione_ (Pezzella and Faggioli, 1999).

Run the Pyomo solver with `--keepfiles` to get the location of the temp problem file (for instance `pyomo solve --solver=cbc --keepfiles pyomo_script.py`).
The [problem.lp](sensitivity/tests/files/problem.lp) problem file (in CPLEX LP format) has been created in this way.

### GLPK files

_Tested with GLPK 5.0 downloaded from https://ftp.gnu.org/gnu/glpk/._

To recreate the GLPK sensitivity report from the [problem.lp](sensitivity/tests/files/problem.lp) problem file, run the following from the same folder:

`$ glpsol --lp problem.lp -o sol_glpk.txt --ranges ranges_glpk.txt`

This recreates the solution and one sensitivity report on both coefficients and constraints.

References:

- Explanation of the format on the [GLPK wiki](https://en.wikibooks.org/wiki/GLPK/Solution_information#Sensitivity_analysis_report)
- Implementation details can be found in the `prrngs.c` file (source)

### CBC files

_Tested with CBC 2.10.7._

To recreate the CBC sensitivity report from the [problem.lp](sensitivity/tests/files/problem.lp) problem file, run the following from the same folder:

`$ cbc problem.lp solve printingOptions all solu sol_cbc.txt printingOptions objective solu obj_cbc.txt printingOptions rhs solu rhs_cbc.txt`

This recreates the solution and two sensitivity reports on coefficients and constraints respectively.

References:

- Example usage of CBC sensitivity report in OpenSolver: https://github.com/AlexMSatalia/OpenSolver/blob/master/OpenSolver.xlam.src/CSolverCbc.cls#L178
- CBC params in the source code: https://github.com/coin-or/Cbc/blob/d4272be8c5e3b231f35e7555587e427a5f69d1ed/src/CbcParameters.cpp#L1192
