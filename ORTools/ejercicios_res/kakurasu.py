"""
Ejercicio 5: Kakurasu 5x5
Tablero de 5x5 donde cada celda puede estar "iluminada" (1) o "apagada" (0).
Las pistas de fila indican la suma de los pesos de las columnas iluminadas.
Las pistas de columna indican la suma de los pesos de las filas iluminadas.

Pesos:
  - Filas:    1, 2, 3, 4, 5 (de arriba hacia abajo)
  - Columnas: 1, 2, 3, 4, 5 (de izquierda a derecha)

Pistas usadas:
  Filas:    [11, 4, 7, 8, 5]
  Columnas: [10, 4, 6, 9, 5]

Nota: aunque el dominio es booleano (0 o 1), se usa model.new_int_var(0, 1)
para mantener la uniformidad con los otros ejercicios. Naturalmente se
podría usar model.new_bool_var().
"""

from ortools.sat.python import cp_model as cp
import numpy as np

#0. Clase de soluciones
class CpSolverSolutionCallbackSon(cp.CpSolverSolutionCallback):
    def __init__(self, matriz):
        super().__init__()
        self.__matriz = matriz
        self.__soluciones = 0
    def OnSolutionCallback(self):
        self.__soluciones+=1
        print(f"Solucion #",self.__soluciones)

        for fila in self.__matriz:
            for valor in fila:
                print(f"{self.value(valor)} ", end=" ")
            print()

#1. Declarar instancia de la clase CpModel()
modelo = cp.CpModel()

#2. Declarar estructura de datos, dominio y variables
matriz_modelo = [ [ modelo.new_int_var(0,1, f"{r}_{c}") for c in range(5) ] for r in range(5) ]

matriz = np.array(matriz_modelo)

#3. Declarar restricciones
filas = [11,4,7,8,5]
columnas = [10,4,6,9,5]

for fila in range(5):
    modelo.add( sum( [matriz[fila][valor-1] * valor for valor in (5,4,3,2,1)] ) == filas[fila])

matriz_tp = matriz.transpose()
for columna in range(5):
    modelo.add( sum( [matriz_tp[columna][valor-1] * valor for valor in (5,4,3,2,1)] ) == columnas[columna])

#4. Declarar solver
solver = cp.CpSolver()
instancia = CpSolverSolutionCallbackSon(matriz)
status = solver.SearchForAllSolutions(modelo, instancia)
