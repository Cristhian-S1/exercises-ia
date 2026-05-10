sudoku = [[0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,3,0,8,5],
           [0,0,1,0,2,0,0,0,0],
           [0,0,0,5,0,7,0,0,0],
           [0,0,4,0,0,0,1,0,0],
           [0,9,0,0,0,0,0,0,0],
           [5,0,0,0,0,0,0,7,3],
           [0,0,2,0,1,0,0,0,0],
           [0,0,0,0,4,0,0,0,9]]

from ortools.sat.python import cp_model
import numpy as np

class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    """SolutionPrinter"""
    def __init__(self, matriz_numpy):
        super().__init__()
        self.__matriz_numpy = matriz_numpy
        self.__solution_count = 0

    def OnSolutionCallback(self):
        self.__solution_count += 1
        print(f'Solution #{self.__solution_count}:')

        for i in range(9):
          for j in range(9):
            print(self.Value(self.__matriz_numpy[i,j]), end=" ")
          print()
        print()

    def SolutionCount(self):
        return self.__solution_count

# 1. La clase CpModel() que viene con el modulo cp_model para crear una instancia
model = cp_model.CpModel()

# 2. Declaracion de las variables de la matriz usando el metodo new_int_var() para variables de tipo IntVar
matriz_model = []
for i in range(9):
    fila = []
    for j in range(9):
        if sudoku[i][j] != 0:
            fila.append(model.new_int_var(sudoku[i][j], sudoku[i][j], f'posicion_1_({i},{j})'))
        else:
            fila.append(model.new_int_var(1,9, f'posicion_0_({i},{j})'))
    matriz_model.append(fila)

matriz_np = np.array(matriz_model)

#3. Las restricciones se declaran mediante metodos que devuelven un objeto de tipo Constraint
# Estas restricciones se guardan en una lista para acumular de forma ordenada 

# Filas y columnas distintas para todos el tablero, todos los numeros de cada cuadrado distintos 
for fila in matriz_np:
    model.add_all_different(fila)

matriz_np_tp = matriz_np.transpose()
for columna in matriz_np_tp:
    model.add_all_different(columna)

for fi,fn in ((0,3),(3,6),(6,9)):
    for ci,cn in ((0,3),(3,6),(6,9)):
        model.add_all_different(matriz_np[fi:fn, ci:cn].flatten())
    
# 4. Clase de CpSolver() que viene con el modulo de cp_model para crear un instancia de resolucion
solver = cp_model.CpSolver()

# status = solver.Solve(model)
solution_printer = SolutionPrinter(matriz_np)

# solution_printer = SimpleSolutionCounter(x)
status = solver.SearchForAllSolutions(model, solution_printer)

if not (status == cp_model.FEASIBLE or status == cp_model.OPTIMAL):
    print("No solution found!")
