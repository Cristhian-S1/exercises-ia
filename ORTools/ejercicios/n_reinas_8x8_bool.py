"""
Ejercicio 4b: N-Reinas 8x8 con matriz booleana (usando NumPy)
Colocar 8 reinas en un tablero 8x8 sin que se ataquen.

En esta versión se usa una matriz booleana b[i][j] organizada con NumPy
para aprovechar .transpose(), .diagonal() y np.fliplr() al construir
las restricciones de columnas y diagonales.

Restricciones:
  1. Exactamente 1 reina por fila
  2. Exactamente 1 reina por columna
  3. A lo sumo 1 reina por diagonal principal (i - j = cte)
  4. A lo sumo 1 reina por diagonal secundaria (i + j = cte)
"""

import numpy as np
from ortools.sat.python import cp_model


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Imprime cada solución del N-Reinas encontrada en formato tablero."""
    def __init__(self, matriz_vars):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__b = matriz_vars
        self.__n = len(matriz_vars)
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        print(f"\nSolución #{self.__solution_count}:")
        for i in range(self.__n):
            fila = []
            for j in range(self.__n):
                val = self.value(self.__b[i][j])
                fila.append("Q" if val == 1 else ".")
            print("  ", " ".join(fila))

    def solution_count(self):
        return self.__solution_count


def resolver_n_reinas_bool(n=8, buscar_todas=False):
    model = cp_model.CpModel()

    # Matriz booleana: b[i][j] = 1 si hay reina en (i, j)
    b = [[model.new_bool_var(f"b_{i}_{j}") for j in range(n)] for i in range(n)]

    # Convertimos a ndarray de objetos para usar métodos NumPy
    matriz = np.array(b, dtype=object)

    # 1. Exactamente 1 reina por fila
    for fila in matriz:
        model.add_exactly_one(fila.tolist())

    # 2. Exactamente 1 reina por columna  (usamos transpose)
    for columna in matriz.T:
        model.add_exactly_one(columna.tolist())

    # 3. A lo sumo 1 reina por diagonal principal
    #    np.diagonal(matriz, offset=k) recorre las diagonales de arriba-izq a abajo-der
    for k in range(-n + 1, n):
        diag = np.diagonal(matriz, offset=k)
        if len(diag) > 1:
            model.add_at_most_one(diag.tolist())

    # 4. A lo sumo 1 reina por diagonal secundaria
    #    Giramos horizontalmente con np.fliplr y luego usamos diagonal
    matriz_flip = np.fliplr(matriz)
    for k in range(-n + 1, n):
        diag = np.diagonal(matriz_flip, offset=k)
        if len(diag) > 1:
            model.add_at_most_one(diag.tolist())

    solver = cp_model.CpSolver()
    solution_printer = SolutionPrinter(b)

    if buscar_todas:
        solver.parameters.enumerate_all_solutions = True
        print(f"Buscando TODAS las soluciones (bool + NumPy) para n={n}...")
    else:
        print(f"Buscando UNA solución (bool + NumPy) para n={n}...")

    status = solver.solve(model, solution_printer)

    print(f"\nStatus: {solver.status_name(status)}")
    print(f"Total de soluciones encontradas: {solution_printer.solution_count()}")


if __name__ == "__main__":
    print("=" * 50)
    print("N-REINAS 8x8 (Bool + NumPy) — Una solución")
    print("=" * 50)
    resolver_n_reinas_bool(n=8, buscar_todas=False)

    print("\n" + "=" * 50)
    print("N-REINAS 8x8 (Bool + NumPy) — Todas las soluciones")
    print("=" * 50)
    resolver_n_reinas_bool(n=8, buscar_todas=True)
