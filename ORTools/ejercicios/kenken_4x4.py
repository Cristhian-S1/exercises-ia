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

from ortools.sat.python import cp_model
import numpy as np


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Imprime cada solución del KenKen encontrada."""
    def __init__(self, matriz_vars):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__matriz = matriz_vars
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        print(f"\nSolución #{self.__solution_count}:")
        for i in range(4):
            fila = [self.value(self.__matriz[i][j]) for j in range(4)]
            print("  ", fila)

    def solution_count(self):
        return self.__solution_count


def resolver_kenken(buscar_todas=False):
    model = cp_model.CpModel()
    n = 4

    # Dominio: enteros del 1 al 4
    x = [[model.new_int_var(1, n, f"x_{i}_{j}") for j in range(n)] for i in range(n)]

    # Restricción de filas y columnas (sin repetir)
    for i in range(n):
        model.add_all_different(x[i])                 # fila
        model.add_all_different([x[j][i] for j in range(n)])  # columna

    # Jaula 1: suma 5 en (0,0) y (1,0)
    model.add(x[0][0] + x[1][0] == 5)

    # Jaula 2: multiplicación 12 en (0,1) y (0,2)
    prod1 = model.new_int_var(1, 16, "prod1")
    model.add_multiplication_equality(prod1, [x[0][1], x[0][2]])
    model.add(prod1 == 12)

    # Jaula 3: resta 1 en (1,1) y (1,2)  -> |a-b| = 1
    b1 = model.new_bool_var("resta_1")
    model.add(x[1][1] - x[1][2] == 1).only_enforce_if(b1)
    model.add(x[1][2] - x[1][1] == 1).only_enforce_if(b1.Not())

    # Jaula 4: división 2 en (0,3) y (1,3) -> max/min = 2
    b2 = model.new_bool_var("div_2")
    model.add(x[0][3] == 2 * x[1][3]).only_enforce_if(b2)
    model.add(x[1][3] == 2 * x[0][3]).only_enforce_if(b2.Not())

    # Jaula 5: suma 5 en (2,0) y (3,0)
    model.add(x[2][0] + x[3][0] == 5)

    # Jaula 6: multiplicación 2 en (2,1) y (3,1)
    prod2 = model.new_int_var(1, 16, "prod2")
    model.add_multiplication_equality(prod2, [x[2][1], x[3][1]])
    model.add(prod2 == 2)

    # Jaula 7: resta 1 en (2,2) y (2,3)
    b3 = model.new_bool_var("resta_2")
    model.add(x[2][2] - x[2][3] == 1).only_enforce_if(b3)
    model.add(x[2][3] - x[2][2] == 1).only_enforce_if(b3.Not())

    # Jaula 8: suma 5 en (3,2) y (3,3)
    model.add(x[3][2] + x[3][3] == 5)

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
    print("KENKEN 4x4 — Una solución")
    print("=" * 50)
    resolver_kenken(buscar_todas=False)

    print("\n" + "=" * 50)
    print("KENKEN 4x4 — Todas las soluciones")
    print("=" * 50)
    resolver_kenken(buscar_todas=True)
