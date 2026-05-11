"""
Ejercicio Practica: Cuadrado de Sumas 4x4

Rellenar una matriz 4x4 con los numeros del 1 al 16 (todos diferentes) tal que
las sumas de filas, columnas y diagonales coincidan con los valores dados.

Datos:
    filas    = [30, 34, 38, 34]
    columnas = [33, 32, 36, 35]
    diagonal principal = 40
    diagonal secundaria = 36

Metodos practicados:
    - model.new_int_var(1, 16) para cada celda
    - model.add_all_different() sobre la matriz aplanada
    - model.add(sum(...) == valor) para filas, columnas y diagonales
    - numpy: np.array, .flatten(), .transpose(), .diagonal(), np.fliplr()
    - SolutionPrinter (CpSolverSolutionCallback)
    - solver.SearchForAllSolutions()
"""

from ortools.sat.python import cp_model as cp
import numpy as np

# 0. Solution callback
class PrintSolutions(cp.CpSolverSolutionCallback):
    def __init__(self, matriz):
        super().__init__()
        self.__matriz = matriz
        self.__count = 0

    def OnSolutionCallback(self):
        self.__count += 1
        print(f"\nSolucion #{self.__count}:")
        for fila in self.__matriz:
            for c in fila:
                print(f"{self.value(c):3d}", end=" ")
            print()

        # Verificar sumas
        for i, fila in enumerate(self.__matriz):
            s = sum(self.value(c) for c in fila)
            print(f"  Fila {i} suma = {s}")
        for j in range(4):
            s = sum(self.value(self.__matriz[i][j]) for i in range(4))
            print(f"  Col {j} suma = {s}")

    @property
    def count(self):
        return self.__count

# 1. Modelo
modelo = cp.CpModel()

# 2. Variables: matriz 4x4 con dominio 1..16
matriz_modelo = [[modelo.new_int_var(1, 16, f"{r}_{c}") for c in range(4)] for r in range(4)]
matriz = np.array(matriz_modelo)

# 3. Restricciones
# Todos los numeros diferentes (aplanar con numpy)
modelo.add_all_different(matriz.flatten())

# Sumas de filas
filas = [30, 34, 38, 34]
for i, fila in enumerate(matriz):
    modelo.add(sum(fila) == filas[i])

# Sumas de columnas (usando .transpose())
columnas = [33, 32, 36, 35]
for j, col in enumerate(matriz.transpose()):
    modelo.add(sum(col) == columnas[j])

# Suma de diagonal principal (usando .diagonal())
modelo.add(sum(matriz.diagonal()) == 40)

# Suma de diagonal secundaria (usando np.fliplr + .diagonal())
modelo.add(sum(np.fliplr(matriz).diagonal()) == 36)

# 4. Solver
solver = cp.CpSolver()
callback = PrintSolutions(matriz)
status = solver.SearchForAllSolutions(modelo, callback)

print(f"\nEstado del solver: {solver.status_name(status)}")
print(f"Total de soluciones: {callback.count}")
