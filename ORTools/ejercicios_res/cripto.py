"""
Ejercicio Practica: Criptoaritmetica SEND + MORE = MONEY

Asignar un digito (0-9) a cada letra tal que:
  - Todas las letras tengan digitos diferentes (add_all_different)
  - S != 0 y M != 0 (primer digito no puede ser cero)
  - Se cumpla la suma columna por columna con acarreo

  Metodos practicados:
    - model.new_int_var() con dominio [0,9] o [1,9]
    - model.new_bool_var() para los acarreos C1, C2, C3
    - model.add_all_different() sobre todas las letras
    - model.add() para las ecuaciones de columna
    - SolutionPrinter (CpSolverSolutionCallback) para imprimir soluciones
    - solver.SearchForAllSolutions()
"""

from ortools.sat.python import cp_model as cp
import numpy as np

#0. Declarar clase de soluciones
class CpSolverSolutionCallbackSon(cp.CpSolverSolutionCallback):
    def __init__(self, lista):
        super().__init__()
        self.__lista = lista
        self.__soluciones = 0
    def OnSolutionCallback(self):
        self.__soluciones+=1
        print(f"Solucion #{self.__soluciones}")
        for valor in self.__lista:
            print(f"{valor} - {self.value(valor)}", end=" ")
        print()

#1. Declarar instancia de CpModel
modelo = cp.CpModel()

#2. Declarar estructura
s = modelo.new_int_var(1,9,'s')
e = modelo.new_int_var(0,9,'e')
n = modelo.new_int_var(0,9,'n')
d = modelo.new_int_var(0,9,'d')

m = modelo.new_int_var(1,9,'m')
o = modelo.new_int_var(0,9,'o')
r = modelo.new_int_var(0,9,'r')

y = modelo.new_int_var(0,9,'y')

lista = [s,e,n,d,m,o,r,y]

#3. Declarar restricciones
modelo.add_all_different(lista)

modelo.add(s*1000+e*100+n*10+d + m*1000+o*100+r*10+e == m*10000+o*1000+n*100+e*10+y)

#4. Solver
solver = cp.CpSolver()
instancia = CpSolverSolutionCallbackSon(lista)
status = solver.SearchForAllSolutions(modelo, instancia)


