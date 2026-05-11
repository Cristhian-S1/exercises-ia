"""
Ejercicio 2: HIDATO 4x4
================================================
Reglas:
1. Rellena el tablero 4x4 con los números del 1 al 16 (sin repetir).
   -> addAllDifferent en toda la matriz aplanada.
2. Los números consecutivos deben estar en celdas ADYACENTES ORTOGONALMENTE
   (arriba, abajo, izquierda, derecha). NO en diagonal.
3. Algunas celdas ya vienen dadas (pistas).

Pistas para este tablero:
    +----+----+----+----+
    |  1 |    |    |  4 |
    +----+----+----+----+
    |    |    |  7 |    |
    +----+----+----+----+
    |    | 10 |    |    |
    +----+----+----+----+
    | 13 |    |    | 16 |
    +----+----+----+----+

Conceptos a practicar:
- new_int_var(1, 16) para cada celda
- addAllDifferent sobre la lista aplanada de 16 variables
- add() para fijar las pistas iniciales
- only_enforce_if() + new_bool_var() para la regla de adyacencia
- numpy para generar los offsets de vecindad: [(-1,0), (1,0), (0,-1), (0,1)]

PISTA DE MODELADO (Adyacencia con only_enforce_if):
La regla "k y k+1 deben ser vecinos" es una implicación para CADA celda:
  "Si celda (i,j) vale k, entonces alguno de sus vecinos vale k+1"

En CP-SAT no puedes escribir directamente un "OR" de ecuaciones.
La forma estándar de modelarlo es:

Para cada celda (i,j) y cada valor k de 1 a 15:
  - Crea una variable booleana auxiliar: b = model.new_bool_var(f"link_{i}_{j}_{k}")
  - Fuerza que b sea 1 exactamente cuando tablero[i][j] == k:
      model.add(tablero[i][j] == k).OnlyEnforceIf(b)
      model.add(tablero[i][j] != k).OnlyEnforceIf(b.Not())
  - Si b es 1 (es decir, esta celda tiene el valor k), entonces la
    suma de las variables booleanas "vecino_vale_k+1" debe ser >= 1.
    Es decir, al menos un vecino ortogonal contiene k+1.

Para detectar "vecino_vale_k+1", crea otra bool por vecino:
  vecino_es_k1 = model.new_bool_var(...)
  model.add(tablero[ni][nj] == k+1).OnlyEnforceIf(vecino_es_k1)
  model.add(tablero[ni][nj] != k+1).OnlyEnforceIf(vecino_es_k1.Not())

Finalmente:
  model.add(sum(vecinos_es_k1) >= 1).OnlyEnforceIf(b)

Esto genera muchas variables bool, pero es el patrón clásico de
"implicación lógica en CP-SAT" que suele caer en prueba.
"""

from ortools.sat.python import cp_model
import numpy as np

# TODO: Completa el modelo siguiendo la pista de modelado

class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, matriz_vars):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__matriz = matriz_vars
        self.__n = len(matriz_vars)
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        print(f"\nSolución #{self.__solution_count}:")
        for i in range(self.__n):
            fila = [self.value(self.__matriz[i][j]) for j in range(self.__n)]
            print("  ", fila)

    def solution_count(self):
        return self.__solution_count


def resolver():
    model = cp_model.CpModel()
    n = 4
    total = n * n  # 16

    # --- TU CÓDIGO AQUÍ ---
    # 1. Crea matriz n x n de new_int_var(1, total)
    # 2. Fija las pistas con add(== ...)
    # 3. addAllDifferent sobre todas las celdas aplanadas
    # 4. Para k=1..total-1, crea las implicaciones de adyacencia con bools
    #    y only_enforce_if. Usa numpy/loops para recorrer vecinos.

    # solver = cp_model.CpSolver()
    # printer = SolutionPrinter(matriz)
    # solver.parameters.enumerate_all_solutions = True
    # status = solver.solve(model, printer)
    # print(f"Status: {solver.status_name(status)}")
    # print(f"Total soluciones: {printer.solution_count()}")


if __name__ == "__main__":
    resolver()
