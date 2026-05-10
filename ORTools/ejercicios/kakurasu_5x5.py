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

from ortools.sat.python import cp_model
import numpy as np


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Imprime cada solución del Kakurasu encontrada."""
    def __init__(self, matriz_vars):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__matriz = matriz_vars
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        print(f"\nSolución #{self.__solution_count}:")
        for i in range(5):
            fila = [self.value(self.__matriz[i][j]) for j in range(5)]
            print("  ", fila)

    def solution_count(self):
        return self.__solution_count


def resolver_kakurasu(buscar_todas=False):
    model = cp_model.CpModel()
    n = 5

    # Dominio: 0 o 1 (booleano modelado como entero)
    x = [[model.new_int_var(0, 1, f"x_{i}_{j}") for j in range(n)] for i in range(n)]

    # Pistas de fila (peso de columna = j+1)
    pistas_fila = [11, 4, 7, 8, 5]
    for i in range(n):
        model.add(sum(x[i][j] * (j + 1) for j in range(n)) == pistas_fila[i])

    # Pistas de columna (peso de fila = i+1)
    pistas_col = [10, 4, 6, 9, 5]
    for j in range(n):
        model.add(sum(x[i][j] * (i + 1) for i in range(n)) == pistas_col[j])

    solver = cp_model.CpSolver()
    solution_printer = SolutionPrinter(x)

    if buscar_todas:
        solver.parameters.enumerate_all_solutions = True
        print("Buscando TODAS las soluciones...")
    else:
        print("Buscando UNA solución...")

    status = solver.solve(model, solution_printer)

    print(f"\nStatus: {solver.status_name(status)}")
    print(f"Total de soluciones encontradas: {solution_printer.solution_count()}")


if __name__ == "__main__":
    print("=" * 50)
    print("KAKURASU 5x5 — Una solución")
    print("=" * 50)
    resolver_kakurasu(buscar_todas=False)

    print("\n" + "=" * 50)
    print("KAKURASU 5x5 — Todas las soluciones")
    print("=" * 50)
    resolver_kakurasu(buscar_todas=True)
