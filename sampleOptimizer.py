from ortools.sat.python import cp_model

class SolutionPrinter(cp_model.CpSolverSolutionCallback) :
    def __init__(self, vars):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__vars = vars
        self.__nsols = 0

    def on_solution_callback(self):
        self.__nsols += 1
        for v in self.__vars:
            print('%s=%i' % (v, self.Value(v)), end=' ')
        print()

    def solution_count(self):
        return self.__solution_count


# Instantiate model and solver
model = cp_model.CpModel()
solver = cp_model.CpSolver()

total_carrying_capacity = 50

quartz = model.NewIntVar(1,total_carrying_capacity, 'quartz')
feldspar = model.NewIntVar(1, total_carrying_capacity, 'feldspar')
gold = model.NewIntVar(1, total_carrying_capacity, 'gold')

solution_printer = SolutionPrinter([quartz, feldspar, gold])

mass_quartz = 4
mass_feldspar = 7
mass_gold = 12

model.Add(quartz * mass_quartz + feldspar * mass_feldspar +
          gold * mass_gold <= total_carrying_capacity)

value_quartz = 3
value_feldspar = 8
value_gold = 12

model.Maximize(value_gold * gold + value_feldspar * feldspar +
               value_quartz * quartz)

solver.parameters.enumerate_all_solutions = True
status = solver.Solve(model, solution_printer)

if status == cp_model.OPTIMAL :
    print("Solution found")
    print("Gold: %i" % solver.Value(gold))
    print("Feldspar: %i" % solver.Value(feldspar))
    print("Quartz: %i" % solver.Value(quartz))
