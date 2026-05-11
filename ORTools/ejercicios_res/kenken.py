"""
Ejercicio 2: KenKen 4x4
Rellenar una matriz 4x4 con números del 1 al 4 tal que:
  - No se repitan en filas ni columnas
  - Se cumplan las operaciones de cada "jaula"

Jaulas definidas:
  - (0,0) + (1,0) = 5               (suma) 
  - (0,1) * (0,2) = 12              (multiplicación)
  - |(1,1) - (1,2)| = 1             (resta)
  - max((0,3),(1,3)) / min((0,3),(1,3)) = 2   (división)
  - (2,0) + (3,0) = 5               (suma)
  - (2,1) * (3,1) = 2               (multiplicación)
  - |(2,2) - (2,3)| = 1             (resta)
  - (3,2) + (3,3) = 5               (suma)

Métodos adicionales usados:
  - model.new_bool_var()  (para modelar la división y la resta con dos ramas)
  - model.add(...).only_enforce_if()  (para forzar una de dos posibilidades)
  - model.add_multiplication_equality()  (para multiplicar dos variables)
"""

from ortools.sat.python import cp_model as cp
import numpy as np

#0. soluciones
class CpSolverSolutionCallbackSon(cp.CpSolverSolutionCallback):
    def __init__(self, matriz):
        super().__init__()
        self.__matriz = matriz
        self.__soluciones = 0

    #on_solution_callback
    def OnSolutionCallback(self):
       print()
       self.__soluciones+=1
       print(f"Solucion #{self.__soluciones}")

       for fila in self.__matriz:
           for valor in fila:
               print(f"{self.value(valor)} ", end=" ")
           print()

#1.modelo
modelo = cp.CpModel()

#2.matriz
matriz_modelo = [ [modelo.new_int_var(1,4, f"{r}_{c}") for c in range(4)] for r in range(4)]
matriz = np.array(matriz_modelo)

#3.restricciones
for fila in matriz:
    modelo.add_all_different(fila)

for columna in matriz.transpose():
    modelo.add_all_different(columna)

#(0,0) + (1,0) = 5
modelo.add(matriz[0][0] + matriz[1][0] == 5)
#(0,1) * (0,2) = 12
modelo.add_multiplication_equality(12, [matriz[0][1], matriz[0][2]])
#|(1,1) - (1,2)| = 1
resta1 = modelo.new_bool_var("resta1")
modelo.add(matriz[1][1] - matriz[1][2] == 1).only_enforce_if(resta1)
modelo.add(matriz[1][2] - matriz[1][1] == 1).only_enforce_if(resta1.Not())
#max((0,3),(1,3)) / min((0,3),(1,3)) = 2
div = modelo.new_bool_var("div")
modelo.add(matriz[0][3] == 2 * matriz[1][3] ).only_enforce_if(div)
modelo.add(matriz[1][3] == 2 * matriz[0][3] ).only_enforce_if(div.Not())
#(2,0) + (3,0) = 5
modelo.add(matriz[2][0] + matriz[3][0] == 5)
#(2,1) * (3,1) = 2
modelo.add_multiplication_equality(2, [matriz[2][1], matriz[3][1]])
#|(2,2) - (2,3)| = 1
resta2 = modelo.new_bool_var("resta2")
modelo.add(matriz[2][2] - matriz[2][3] == 1).only_enforce_if(resta2)
modelo.add(matriz[2][3] - matriz[2][2] == 1).only_enforce_if(resta2.Not())
#(3,2) + (3,3) = 5
modelo.add(matriz[3][2] + matriz[3][3] == 5)

#4. solver
solver = cp.CpSolver()
instancia = CpSolverSolutionCallbackSon(matriz)
status = solver.SearchForAllSolutions(modelo, instancia)
