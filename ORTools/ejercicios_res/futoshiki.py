"""
Ejercicio 3: Futoshiki 4x4
Rellenar una matriz 4x4 con números del 1 al 4 tal que:
  - No se repitan en filas ni columnas
  - Se respeten las desigualdades entre celdas adyacentes

Desigualdades definidas:
  - x[0][0] > x[0][1]
  - x[0][2] < x[0][3]
  - x[1][0] < x[2][0]
  - x[1][2] > x[1][3]

  - x[2][1] > x[2][2]
  - x[3][0] < x[3][1]
  - x[3][2] > x[3][3]
  - x[1][1] < x[2][1]

  - x[0][1] > x[1][1]
"""

from ortools.sat.python import cp_model as cp
import numpy as np

#0. Declarar clase para soluciones
class CpSolverSolutionCallbackSon(cp.CpSolverSolutionCallback):
    def __init__(self, matriz):
        super().__init__()
        self.__matriz = matriz
        self.__contador_soluciones = 0

    def OnSolutionCallback(self):
        self.__contador_soluciones+=1
        print(f"Solucion #{self.__contador_soluciones}")

        for fila in self.__matriz:
            print()
            for valor in fila:
                print(self.value(valor)," ", end=" ")
            print()

#1. Declarar la instancia de la clase CpSolver()
modelo = cp.CpModel()

#2. Declarar estructura de datos, variables y dominios
matriz_model = [ [modelo.new_int_var(1,4, f"{r}_{c}") for c in range(4) ]  for r in range(4) ]

matriz = np.array(matriz_model)

#3. Declarar restricciones
for fila in matriz:
    modelo.add_all_different(fila)

for columna in matriz.transpose():
    modelo.add_all_different(columna)

restricciones = [matriz[0][0],matriz[0][1], matriz[0][3],matriz[0][2], matriz[2,0],matriz[1][0], matriz[1][2],matriz[1][3],
                matriz[2][1],matriz[2][2], matriz[3][1],matriz[3][0], matriz[3][2],matriz[3][3], matriz[2][1],matriz[1][1],
                matriz[0][1],matriz[1][1]  ]

for i in range(0, len(restricciones)-1, 2):
    modelo.add(restricciones[i] > restricciones[i+1])

#4. Declarar solver
solver = cp.CpSolver()
instancia = CpSolverSolutionCallbackSon(matriz)
status = solver.SearchForAllSolutions(modelo, instancia)
