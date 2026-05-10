"""
Ejemplo: encontrar una solución factible
Comencemos con un problema de ejemplo sencillo en el que hay lo siguiente:

    - Tres variables, x, y, y z, cada una de las cuales puede asumir los valores: 0, 1 o 2.
    - Una restricción: x != y

"""

from ortools.sat.python import cp_model

#Usamos la clase CpModel() que viene con el modulo de cp_model
#para crear una instancia 
model = cp_model.CpModel() 

#Declaramos variables de tipo IntVar usando el metodo new_int_var()
#la instancia model va acumulando las definiciones del problema, tanto dominios como restricciones
x = model.new_int_var(0, 2, "x")
y = model.new_int_var(0, 2, "y")
z = model.new_int_var(0, 2, "z")

#Agregamos la restriccion usando el metodo add() que devuelve un objeto de tipo Constraint
model.add(x != y)

#Usamos la clase de CpSolver() que viene con el modulo de co_model
#para crear una instancia
solver = cp_model.CpSolver()
status = solver.solve(model)

#El modulo cp_model viene con constantes que en teoria son enums
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(f"x = {solver.value(x)}")
    print(f"y = {solver.value(y)}")
    print(f"z = {solver.value(z)}")
else:
    print("No solution found.")