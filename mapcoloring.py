from ortools.sat.python import cp_model

# Instantiate model and solver
model = cp_model.CpModel()
solver = cp_model.CpSolver()

## colors: 0: Red, 1: Blue 2: Green
colors = {0 : 'Red',1:'Blue',2:'Green'}

SF = model.NewIntVar(0,2,'SF')
Alameda = model.NewIntVar(0,2,'Alameda')
Marin = model.NewIntVar(0,2,'Marin')
SanMateo = model.NewIntVar(0,2,'San Mateo')
SantaClara = model.NewIntVar(0,2,'Santa Clara')
ContraCosta = model.NewIntVar(0,2,'Contra Costa')
Solano = model.NewIntVar(0,2,'Solano')
Napa = model.NewIntVar(0,2,'Napa')
Sonoma = model.NewIntVar(0,2,'Sonoma')

## add edges
model.Add(SF != Alameda)
model.Add(SF != Marin)
model.Add(SF != SanMateo)
model.Add(ContraCosta != Alameda)
model.Add(Alameda != SanMateo)
model.Add(Alameda != SantaClara)
model.Add(SantaClara != SanMateo)
model.Add(Marin != Sonoma)
model.Add(Sonoma != Napa)
model.Add(Napa != Solano)
model.Add(Solano != ContraCosta)
model.Add(ContraCosta != Marin)

status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print("SF: %s" % colors[solver.Value(SF)])
    print("Alameda: %s" % colors[solver.Value(Alameda)])
    print("Marin: %s" % colors[solver.Value(Marin)])
    print("Contra Costa: %s" % colors[solver.Value(ContraCosta)])
    print("Solano: %s" % colors[solver.Value(Solano)])
    print("Sonoma: %s" % colors[solver.Value(Sonoma)])
    print("Santa Clara: %s" % colors[solver.Value(SantaClara)])
    print("San Mateo: %s" % colors[solver.Value(SanMateo)])
    print("Napa: %s" % colors[solver.Value(Napa)])


