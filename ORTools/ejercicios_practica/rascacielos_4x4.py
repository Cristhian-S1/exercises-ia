"""
Ejercicio 1: SKYSCRAPERS (Rascacielos) 4x4
================================================
Reglas:
1. Rellena el tablero 4x4 con números del 1 al 4.
2. Cada fila y cada columna deben contener todos los números del 1 al 4
   (sin repetir). -> addAllDifferent
3. Las pistas en los bordes indican CUÁNTOS edificios se ven mirando
   desde esa dirección. Los edificios más altos tapan a los más bajos
   que estén detrás.

Pistas para este tablero:
      2   1   2   3
    +---+---+---+---+
  2 |   |   |   |   | 2
    +---+---+---+---+
  3 |   |   |   |   | 1
    +---+---+---+---+
  1 |   |   |   |   | 2
    +---+---+---+---+
  2 |   |   |   |   | 2
    +---+---+---+---+
      2   3   2   1

Conceptos a practicar:
- new_int_var() con dominio 1..4
- addAllDifferent() por filas y columnas (usa numpy .T para columnas)
- add() para restricciones lineales de visibilidad
- (Opcional/Difícil) new_bool_var + only_enforce_if para modelar el
  conteo exacto de edificios visibles desde cada borde.

PISTA DE MODELADO (Visibilidad):
La forma más sencilla de modelar "cuántos se ven desde la izquierda"
es crear variables booleanas auxiliares que indiquen si una celda es
el máximo acumulado hasta ese punto.

Por ejemplo, para la fila i vista desde la izquierda:
  visible[i][0] == 1  (el primero siempre se ve)
  visible[i][j] == 1  SI Y SOLO SI  altura[i][j] > max(altura[i][0..j-1])
Luego la suma de visibles debe ser igual a la pista del borde.

Para evitar el max(), puedes usar solo bools y only_enforce_if:
  Para j>0 y k<j:
    Si altura[i][j] > altura[i][k], entonces visible[i][j] puede ser 1
    Si altura[i][j] < altura[i][k], entonces no puede ser visible.
  visible[i][j] == 1  =>  altura[i][j] > altura[i][k] para todo k<j
Esto es más avanzado; una versión de examen suele darte una pista más
simple o aceptar el modelo con variables auxiliares.
"""

from ortools.sat.python import cp_model
import numpy as np

# TODO: Completa el modelo
# 1. Crea la matriz 4x4 de new_int_var(1, 4)
# 2. Aplica addAllDifferent en filas y columnas (usa matriz.T)
# 3. Implementa las restricciones de visibilidad según las pistas

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

    # --- TU CÓDIGO AQUÍ ---
    # matriz = ...

    # solver = cp_model.CpSolver()
    # printer = SolutionPrinter(matriz)
    # solver.parameters.enumerate_all_solutions = True
    # status = solver.solve(model, printer)
    # print(f"Status: {solver.status_name(status)}")
    # print(f"Total soluciones: {printer.solution_count()}")


if __name__ == "__main__":
    resolver()
