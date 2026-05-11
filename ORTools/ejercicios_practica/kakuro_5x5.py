"""
Ejercicio 3: KAKURO 5x5 simplificado
================================================
Reglas:
1. El tablero es una cuadrícula 5x5 donde algunas celdas son "negras"
   (bloqueadas) y otras son "blancas" (rellenables).
2. En cada celda blanca debes poner un dígito del 1 al 9.
3. Una "entrada" es una secuencia máxima de celdas blancas consecutivas
   en horizontal o vertical.
4. Para cada entrada se da una PISTA (suma total) y los dígitos dentro
   de una misma entrada NO se pueden repetir.
   -> addAllDifferent dentro de cada entrada
   -> add(sum(entrada) == pista)

Tablero (X = negra/bloqueada, . = blanca/rellenable):

      0   1   2   3   4
    +---+---+---+---+---+
  0 | X | X | . | . | X |   Entrada Horizontal (0,2)-(0,3): suma = 10
    +---+---+---+---+---+   Entrada Vertical (0,2)-(1,2): suma = 12
  1 | X | . | . | . | . |   Entrada Horizontal (1,1)-(1,4): suma = 11
    +---+---+---+---+---+   Entrada Vertical (0,3)-(1,3): suma = 5
  2 | . | . | X | . | . |   Entrada Horizontal (2,0)-(2,1): suma = 8
    +---+---+---+---+---+   Entrada Vertical (2,0)-(3,0)-(4,0): suma = 12
  3 | . | X | . | . | X |   Entrada Horizontal (2,3)-(2,4): suma = 8
    +---+---+---+---+---+   Entrada Vertical (1,4)-(2,4): suma = 6
  4 | . | X | X | . | X |   Entrada Horizontal (3,0): (solo 1 celda, suma=4)
    +---+---+---+---+---+   Entrada Horizontal (3,2)-(3,3): suma = 6
                            Entrada Horizontal (4,0): suma = 3
                            Entrada Horizontal (4,3): suma = 4
                            Entrada Vertical (2,1)-(3,1): ya está bloqueada en 3,1
                            Entrada Vertical (2,3)-(3,3)-(4,3): suma = 13

Conceptos a practicar:
- new_int_var(1, 9) solo para celdas blancas (o usa 0 para negras)
- addAllDifferent() sobre listas de variables que forman cada entrada
- add(sum(...) == pista) para cada entrada
- numpy/matriz para definir la estructura del tablero y las entradas
  (puedes usar una matriz de enteros donde -1 es negra, 0 es blanca,
  y luego recorrer con numpy/loops para detectar entradas horizontales
  y verticales).

PISTA DE MODELADO:
Define primero el tablero como una matriz numpy de objetos:
  tablero = np.full((5,5), None, dtype=object)
Para cada celda blanca (i,j):
  tablero[i][j] = model.new_int_var(1, 9, f"c_{i}_{j}")
Para cada celda negra:
  tablero[i][j] = None   (o un placeholder)

Luego define manualmente (o algorítmicamente) las listas de variables
que forman cada entrada. Por ejemplo:
  entrada_h1 = [tablero[0][2], tablero[0][3]]
  model.add(sum(entrada_h1) == 10)
  model.add_all_different(entrada_h1)

Si quieres hacerlo algorítmico (más numpy), recorre cada fila y
extrae slices de celdas blancas consecutivas entre celdas negras.
"""

from ortools.sat.python import cp_model
import numpy as np

# TODO: Completa el modelo

class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, matriz_vars, mascara_negras):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__matriz = matriz_vars
        self.__negras = mascara_negras
        self.__n = len(matriz_vars)
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        print(f"\nSolución #{self.__solution_count}:")
        for i in range(self.__n):
            fila = []
            for j in range(self.__n):
                if self.__negras[i][j]:
                    fila.append("X")
                else:
                    fila.append(str(self.value(self.__matriz[i][j])))
            print("  ", " ".join(fila))

    def solution_count(self):
        return self.__solution_count


def resolver():
    model = cp_model.CpModel()
    n = 5

    # Máscara de celdas negras: True = bloqueada, False = rellenable
    negras = np.array([
        [True,  True,  False, False, True ],
        [True,  False, False, False, False],
        [False, False, True,  False, False],
        [False, True,  False, False, True ],
        [False, True,  True,  False, True ],
    ])

    # --- TU CÓDIGO AQUÍ ---
    # 1. Crea la matriz de variables (None para negras, new_int_var para blancas)
    # 2. Define las entradas horizontales y verticales con sus sumas
    # 3. Aplica add(sum(entrada) == pista) y addAllDifferent(entrada)
    #    para cada entrada de longitud > 1.

    # solver = cp_model.CpSolver()
    # printer = SolutionPrinter(tablero, negras)
    # solver.parameters.enumerate_all_solutions = True
    # status = solver.solve(model, printer)
    # print(f"Status: {solver.status_name(status)}")
    # print(f"Total soluciones: {printer.solution_count()}")


if __name__ == "__main__":
    resolver()
