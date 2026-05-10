"""
Maximiza 2x + 2y + 3z sujeto a las siguientes restricciones:
    2x + 7y + 3z	≤	50
    3x - 5y + 7z	≤	45
    5x + 2y - 6z	≤	37
    x, y, z	 ≥	0
    Números enteros x, y, z
"""
from ortools.sat.python import cp_model

#1. Declaramos el modelo
model = cp_model.CpModel()

#2. Creamos las variables
var_upper_limit = max(50,45,37)
print(var_upper_limit)

x = model.new_int_var(0, var_upper_limit, "x")
y = model.new_int_var(0, var_upper_limit, "y")
z = model.new_int_var(0, var_upper_limit, "z")

#3. Restricciones
model.add(2*x + 7*y + 3*z <= 50)
model.add(3*x - 5*y + 7*z <= 45)
model.add(5*x + 2*y - 6*z <= 37)

model.maximize(2*x + 2*y + 3*z)

#4. Solver
solver = cp_model.CpSolver()
status = solver.solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(f"Maximum of objective function: {solver.objective_value}\n")
    print(f"x = {solver.value(x)}")
    print(f"y = {solver.value(y)}")
    print(f"z = {solver.value(z)}")
else:
    print("No solution found.")