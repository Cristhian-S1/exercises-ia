"""
Ejercicio 1: Cuadrado Mágico 3x3
Colocar los números del 1 al 9 en una matriz 3x3 tal que:
  - Todas las filas sumen 15
  - Todas las columnas sumen 15
  - Ambas diagonales sumen 15
  - No se repitan números

Se muestra una solución y luego se enumeran todas las soluciones únicas
usando SolutionPrinter (CpSolverSolutionCallback).
"""

from ortools.sat.python import cp_model
import numpy as np


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Imprime cada solución del cuadrado mágico encontrada."""
    def __init__(self, matriz_vars):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__matriz = matriz_vars
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        print(f"\nSolución #{self.__solution_count}:")
        for i in range(3):
            fila = [self.value(self.__matriz[i][j]) for j in range(3)]
            print("  ", fila)
        # Suma mágica de referencia
        print(f"  Suma fila 0 = {sum(self.value(self.__matriz[0][j]) for j in range(3))}")

    def solution_count(self):
        return self.__solution_count


def resolver_cuadrado_magico(buscar_todas=False):
    model = cp_model.CpModel()
    n = 3
    suma_magica = 15

    # Dominio: enteros del 1 al 9
    x = [[model.new_int_var(1, 9, f"x_{i}_{j}") for j in range(n)] for i in range(n)]

    # Todas las celdas deben ser diferentes
    model.add_all_different(np.array(x).flatten().tolist())

    # Restricciones de sumas
    for i in range(n):
        model.add(sum(x[i][j] for j in range(n)) == suma_magica)  # filas
        model.add(sum(x[j][i] for j in range(n)) == suma_magica)  # columnas

    # Diagonales
    model.add(sum(x[i][i] for i in range(n)) == suma_magica)
    model.add(sum(x[i][n - 1 - i] for i in range(n)) == suma_magica)

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
    print("CUADRADO MÁGICO 3x3 — Una solución")
    print("=" * 50)
    resolver_cuadrado_magico(buscar_todas=False)

    print("\n" + "=" * 50)
    print("CUADRADO MÁGICO 3x3 — Todas las soluciones")
    print("=" * 50)
    resolver_cuadrado_magico(buscar_todas=True)
