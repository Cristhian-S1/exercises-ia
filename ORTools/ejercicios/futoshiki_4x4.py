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

from ortools.sat.python import cp_model


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Imprime cada solución del Futoshiki encontrada."""
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


def resolver_futoshiki(buscar_todas=False):
    model = cp_model.CpModel()
    n = 4

    # Dominio: enteros del 1 al 4
    x = [[model.new_int_var(1, n, f"x_{i}_{j}") for j in range(n)] for i in range(n)]

    # Restricción de filas y columnas (sin repetir)
    for i in range(n):
        model.add_all_different(x[i])
        model.add_all_different([x[j][i] for j in range(n)])

    # Desigualdades
    model.add(x[0][0] > x[0][1])
    model.add(x[0][2] < x[0][3])
    model.add(x[1][0] < x[2][0])
    model.add(x[1][2] > x[1][3])
    model.add(x[2][1] > x[2][2])
    model.add(x[3][0] < x[3][1])
    model.add(x[3][2] > x[3][3])
    model.add(x[1][1] < x[2][1])
    model.add(x[0][1] > x[1][1])

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
    print("FUTOSHIKI 4x4 — Una solución")
    print("=" * 50)
    resolver_futoshiki(buscar_todas=False)

    print("\n" + "=" * 50)
    print("FUTOSHIKI 4x4 — Todas las soluciones")
    print("=" * 50)
    resolver_futoshiki(buscar_todas=True)
