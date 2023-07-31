from pyomo.environ import ConcreteModel, Suffix, Var, SolverFactory, NonNegativeReals, minimize

supply_vals = [90, 85, 100, 95]
demand_vals = [45, 38, 15, 40, 25, 20, 29, 23, 34, 55, 28, 18]
cost_vals = [
    [28, 40, 25, 58, 64, 55, 79, 77, 100, 118, 125, 110],
    [55, 28, 36, 25, 15, 38, 29, 45, 49, 68, 82, 72],
    [80, 53, 71, 37, 23, 65, 25, 60, 27, 47, 73, 75],
    [135, 108, 112, 94, 77, 88, 52, 64, 35, 14, 35, 48],
]

supply = dict(zip([f"{i + 1}" for i in range(len(supply_vals))], supply_vals))
demand = dict(zip([f"{i + 1}" for i in range(len(demand_vals))], demand_vals))
cost = dict(
    ((f"{i + 1}", f"{j + 1}"), cost_vals[i][j]) for i in range(len(supply_vals)) for j in range(len(demand_vals))
)

# Step 0: Create an instance of the model
model = ConcreteModel()
model.dual = Suffix(direction=Suffix.IMPORT)

# Step 1: Define index sets
SRC = list(supply.keys())
DST = list(demand.keys())

# Step 2: Define the decision
model.x = Var(SRC, DST, domain=NonNegativeReals)


# Step 3: Define Objective
@model.Objective(sense=minimize)
def cost_func(m):
    return sum([cost[s, d] * model.x[s, d] for s in SRC for d in DST])


# Step 4: Constraints
@model.Constraint(DST)
def dst(m, d):
    return sum([model.x[s, d] for s in SRC]) == demand[d]


@model.Constraint(SRC)
def src(m, s):
    return sum([model.x[s, d] for d in DST]) == supply[s]


results = SolverFactory("glpk").solve(model)
results.write()
