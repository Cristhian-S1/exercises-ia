"""
Ejercicio 4: N-Reinas 8x8
Colocar 8 reinas en un tablero de ajedrez 8x8 de forma que ninguna se ataque.
En lugar de una matriz booleana, se usa un vector q[i] = columna de la reina en la fila i.
Esto garantiza una única reina por fila automáticamente.

Restricciones:
  - Columnas distintas (sin ataques verticales)
  - Diagonales principales distintas
  - Diagonales secundarias distintas

Se muestra una solución y luego se enumeran todas las soluciones posibles.
"""

from ortools.sat.python import cp_model


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Imprime cada solución del N-Reinas encontrada en formato tablero."""
    def __init__(self, reinas_vars):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__q = reinas_vars
        self.__n = len(reinas_vars)
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        print(f"\nSolución #{self.__solution_count}:")
        for i in range(self.__n):
            col = self.value(self.__q[i])
            fila = ["."] * self.__n
            fila[col] = "Q"
            print("  ", " ".join(fila))

    def solution_count(self):
        return self.__solution_count


def resolver_n_reinas(n=8, buscar_todas=False):
    model = cp_model.CpModel()

    # q[i] = columna de la reina en la fila i
    q = [model.new_int_var(0, n - 1, f"q_{i}") for i in range(n)]

    # Ninguna comparte columna
    model.add_all_different(q)

    # Variables auxiliares para diagonales
    diag1 = [model.new_int_var(0, 2 * n - 2, f"d1_{i}") for i in range(n)]  # q[i] + i
    diag2 = [model.new_int_var(-(n - 1), n - 1, f"d2_{i}") for i in range(n)]  # q[i] - i

    for i in range(n):
        model.add(diag1[i] == q[i] + i)
        model.add(diag2[i] == q[i] - i)

    model.add_all_different(diag1)
    model.add_all_different(diag2)

    solver = cp_model.CpSolver()
    solution_printer = SolutionPrinter(q)

    if buscar_todas:
        solver.parameters.enumerate_all_solutions = True
        print(f"Buscando TODAS las soluciones para n={n}...")
    else:
        print(f"Buscando UNA solución para n={n}...")

    status = solver.solve(model, solution_printer)

    print(f"\nStatus: {solver.status_name(status)}")
    print(f"Total de soluciones encontradas: {solution_printer.solution_count()}")


if __name__ == "__main__":
    print("=" * 50)
    print("N-REINAS 8x8 — Una solución")
    print("=" * 50)
    resolver_n_reinas(n=8, buscar_todas=False)

    print("\n" + "=" * 50)
    print("N-REINAS 8x8 — Todas las soluciones")
    print("=" * 50)
    resolver_n_reinas(n=8, buscar_todas=True)
