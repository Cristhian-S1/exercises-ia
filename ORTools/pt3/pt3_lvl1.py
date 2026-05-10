"""Para CP + IS + DIV = VERDADERO, las restricciones son las siguientes:

    La ecuación: CP + IS + FUN = TRUE.
    Cada una de las diez letras debe ser un dígito diferente.
    C, I, F y T no pueden ser cero (ya que no se escriben ceros a la izquierda en números).
"""

from ortools.sat.python import cp_model 
from pt3.pt3_lvl2_class_printer import VarArraySolutionPrinter
#1. Declaramos el modelo 
model = cp_model.CpModel()

#2. Declaramos el dominio 

c = model.new_int_var(1, 9, "c")
p = model.new_int_var(0, 9, "p")
i = model.new_int_var(1, 9, "i")
s = model.new_int_var(0, 9, "s")
f = model.new_int_var(1, 9, "f")
u = model.new_int_var(0, 9, "u")
n = model.new_int_var(0, 9, "n")
t = model.new_int_var(1, 9, "t")
r = model.new_int_var(0, 9, "r")
e = model.new_int_var(0, 9, "e")

#3. Declaramos las restricciones
model.add(c*10+p + i*10+s + f*100+u*10+n == t*1000+r*100+u*10+e  )

charts = [c,p,i,s,f,u,n,t,r,e]
model.add_all_different(charts)

#4. Declaramos el solver
solver = cp_model.CpSolver()
solution_printer = VarArraySolutionPrinter(charts)

solver.parameters.enumerate_all_solutions = True
status = solver.solve(model, solution_printer)

print(f"solutions found: {solution_printer.solution_count}")