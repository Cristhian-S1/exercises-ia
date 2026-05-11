"""
Ejercicio Practica: Criptoaritmetica SEND + MORE = MONEY

Asignar un digito (0-9) a cada letra tal que:
  - Todas las letras tengan digitos diferentes (add_all_different)
  - S != 0 y M != 0 (primer digito no puede ser cero)
  - Se cumpla la suma columna por columna con acarreo

  Metodos practicados:
    - model.new_int_var() con dominio [0,9] o [1,9]
    - model.new_bool_var() para los acarreos C1, C2, C3
    - model.add_all_different() sobre todas las letras
    - model.add() para las ecuaciones de columna
    - SolutionPrinter (CpSolverSolutionCallback) para imprimir soluciones
    - solver.SearchForAllSolutions()
"""

from ortools.sat.python import cp_model as cp

# 0. Solution callback
class PrintSolutions(cp.CpSolverSolutionCallback):
    def __init__(self, letras):
        super().__init__()
        self.__letras = letras
        self.__count = 0

    def OnSolutionCallback(self):
        self.__count += 1
        S = self.value(self.__letras[0])
        E = self.value(self.__letras[1])
        N = self.value(self.__letras[2])
        D = self.value(self.__letras[3])
        M = self.value(self.__letras[4])
        O = self.value(self.__letras[5])
        R = self.value(self.__letras[6])
        Y = self.value(self.__letras[7])
        C1 = self.value(self.__letras[8])
        C2 = self.value(self.__letras[9])
        C3 = self.value(self.__letras[10])

        print(f"\nSolucion #{self.__count}")
        print(f"   {S}{E}{N}{D}")
        print(f"+  {M}{O}{R}{E}")
        print(f"-----------")
        print(f"  {M}{O}{N}{E}{Y}")
        print(f"Acarreos: C1={C1}, C2={C2}, C3={C3}")

    @property
    def count(self):
        return self.__count

# 1. Modelo
modelo = cp.CpModel()

# 2. Variables
# Letras: S, E, N, D, M, O, R, Y
# S y M no pueden ser 0 (primer digito de cada numero)
S = modelo.new_int_var(1, 9, 'S')
E = modelo.new_int_var(0, 9, 'E')
N = modelo.new_int_var(0, 9, 'N')
D = modelo.new_int_var(0, 9, 'D')
M = modelo.new_int_var(1, 9, 'M')
O = modelo.new_int_var(0, 9, 'O')
R = modelo.new_int_var(0, 9, 'R')
Y = modelo.new_int_var(0, 9, 'Y')

# Acarreos (0 o 1)  --  new_bool_var
C1 = modelo.new_bool_var('C1')
C2 = modelo.new_bool_var('C2')
C3 = modelo.new_bool_var('C3')

letras = [S, E, N, D, M, O, R, Y, C1, C2, C3]

# 3. Restricciones
# Todos los digitos de letras diferentes
modelo.add_all_different([S, E, N, D, M, O, R, Y])

# Ecuaciones por columna (de derecha a izquierda):
# Columna 0 (unidades):      D + E = Y + 10*C1
modelo.add(D + E == Y + 10 * C1)

# Columna 1 (decenas):       N + R + C1 = E + 10*C2
modelo.add(N + R + C1 == E + 10 * C2)

# Columna 2 (centenas):      E + O + C2 = N + 10*C3
modelo.add(E + O + C2 == N + 10 * C3)

# Columna 3 (millares):      S + M + C3 = O + 10*M
modelo.add(S + M + C3 == O + 10 * M)

# 4. Solver
solver = cp.CpSolver()
callback = PrintSolutions(letras)
status = solver.SearchForAllSolutions(modelo, callback)

print(f"\nEstado del solver: {solver.status_name(status)}")
print(f"Total de soluciones: {callback.count}")
