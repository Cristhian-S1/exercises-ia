"""
Ejemplo: encontrar una solución factible
Comencemos con un problema de ejemplo sencillo en el que hay lo siguiente:

    - Tres variables, x, y, y z, cada una de las cuales puede asumir los valores: 0, 1 o 2.
    - Una restricción: x != y
"""

from ortools.sat.python import cp_model
from pt1.pt1_lvl2_class_printer import VarArraySolutionPrinter

#Usamos la clase CpModel() que viene con el modulo de cp_model
#para crear una instancia 
model = cp_model.CpModel() 

#Declaramos variables de tipo IntVar usando el metodo new_int_var()
x = model.new_int_var(0, 2, "x")
y = model.new_int_var(0, 2, "y")
z = model.new_int_var(0, 2, "z")

#Agregamos la restriccion usando el metodo add() que devuelve un objeto de tipo Constraint
#Estas restricciones se guardan en una lista y no como set porque requiere mantener el orden
#y permitir multiples restricciones independientes 
model.add(x != y)

#Usamos la clase de CpSolver() que viene con el modulo de cp_model
#para crear una instancia
solver = cp_model.CpSolver()
solution_printer = VarArraySolutionPrinter([x, y ,z])

#Soluciones
solver.parameters.enumerate_all_solutions = True
status = solver.solve(model, solution_printer)

print(f"Status = {solver.status_name(status)}")
print(f"Number of solutions found: {solution_printer.solution_count}")
