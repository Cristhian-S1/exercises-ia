""" Ejercicio 1: Cuadrado Mágico 3x3
Colocar los números del 1 al 9 en una matriz 3x3 tal que:
  - Todas las filas sumen 15
  - Todas las columnas sumen 15
  - Ambas diagonales sumen 15
  - No se repitan números

Se muestra una solución y luego se enumeran todas las soluciones únicas
usando SolutionPrinter (CpSolverSolutionCallback). """

from ortools.sat.python import cp_model as cp
import numpy as np

class CpSolverSolutionCallbackSon(cp.CpSolverSolutionCallback):
    def __init__(self, matriz):
        super().__init__()
        self.__matriz = matriz
        self.__soluciones = 0

    def OnSolutionCallback(self):
        self.__soluciones+=1
        print(f"Solucion #{self.__soluciones}")

        for r in self.__matriz:
            for c in r:
                print(f"valor {self.value(c)}", end=" ")
            print()
        print()

#1. Declarar la instancia de la clase CpModel()
modelo = cp.CpModel()

#2. Declarar la matriz junto a sus variables
matriz_modelo = [ [modelo.new_int_var(1,9, f"{r}_{c}") for c in range(3) ] for r in range(3) ]
matriz = np.array(matriz_modelo)

#3. Declarar restricciones

for fila in matriz:
    modelo.add(sum(fila) == 15)

matriz_transpuesta = matriz.transpose()
for columna in matriz_transpuesta:
    modelo.add(sum(columna) == 15)

matriz_diagonal = matriz.diagonal()
modelo.add(sum(matriz_diagonal) == 15)

matriz_flip = np.fliplr(matriz)
matriz_flip_diagonal = matriz_flip.diagonal()
modelo.add(sum(matriz_flip_diagonal) == 15)

matriz_flat = matriz.flatten()
modelo.add_all_different(matriz_flat)

#4. Solver
solver = cp.CpSolver()
cp_solver_solution_callback = CpSolverSolutionCallbackSon(matriz)
status = solver.SearchForAllSolutions(modelo, cp_solver_solution_callback)




"""
status = solver.solve(modelo)
if status == cp.OPTIMAL or status == cp.FEASIBLE:
    for r in matriz:
        print()
        for c in r:
            print(f"valor {solver.value(c)}", end=" ")
        print()
"""





