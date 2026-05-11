"""
Ejercicio Practica: Seleccion de Objetos (Mochila con Restricciones)

Seleccionar un subconjunto de 8 objetos que maximice el valor total,
respetando el peso maximo de la mochila y restricciones logicas adicionales.

                     Objeto:  0   1   2   3   4   5   6   7
Datos de entrada:     Peso:   4   3   5   2   6   1   3   2
                     Valor:  10   6  12   5  15   3   7   4

Capacidad maxima de la mochila: 14

Restricciones adicionales:
  1) Si se selecciona el objeto 0, obligatoriamente el objeto 1 tambien.
  2) Los objetos 2 y 3 no pueden seleccionarse simultaneamente.
  3) Se deben seleccionar entre 3 y 5 objetos en total.
  4) Al menos 2 objetos de entre los ultimos 4 (objetos 4, 5, 6, 7) deben
     estar seleccionados.

Objetivo: Maximizar el valor total de los objetos seleccionados.

Metodos practicados:
  - model.new_bool_var() para cada objeto (seleccionado o no)
  - model.add(sum(pesos * vars) <= capacidad)  (restriccion de peso)
  - model.add(sum(vars) >= k) y model.add(sum(vars) <= m)  (cantidad)
  - Expresion de condiciones logicas con desigualdades lineales:
      x[0] <= x[1]          (si 0 entonces 1)
      x[2] + x[3] <= 1      (conflicto, a lo sumo uno)
  - model.Maximize(valor_total) para optimizar
  - SolutionPrinter (CpSolverSolutionCallback) para mostrar la solucion
  - solver.SearchForAllSolutions() y solver.value() para la solucion optima
"""

from ortools.sat.python import cp_model as cp

# 0. Solution callback
class PrintSolutions(cp.CpSolverSolutionCallback):
    def __init__(self, x):
        super().__init__()
        self.__x = x
        self.__count = 0

    def OnSolutionCallback(self):
        self.__count += 1
        seleccionados = [i for i in range(8) if self.value(self.__x[i]) == 1]
        peso_total = sum(pesos[i] for i in seleccionados)
        valor_total = sum(valores[i] for i in seleccionados)

        print(f"\nSolucion #{self.__count}")
        print(f"  Objetos seleccionados: {seleccionados}")
        print(f"  Peso total: {peso_total} / 14")
        print(f"  Valor total: {valor_total}")

    @property
    def count(self):
        return self.__count

# Datos
pesos = [4, 3, 5, 2, 6, 1, 3, 2]
valores = [10, 6, 12, 5, 15, 3, 7, 4]
capacidad = 14

# 1. Modelo
modelo = cp.CpModel()

# 2. Variables: new_bool_var para cada objeto
x = [modelo.new_bool_var(f"x_{i}") for i in range(8)]

# 3. Restricciones

# 3a. Peso maximo
modelo.add(sum(x[i] * pesos[i] for i in range(8)) <= capacidad)

# 3b. Cantidad de objetos: entre 3 y 5
modelo.add(sum(x) >= 3)
modelo.add(sum(x) <= 5)

# 3c. Si se selecciona el 0, tambien el 1  (x[0] -> x[1]  equivale a  x[0] <= x[1])
modelo.add(x[0] <= x[1])

# 3d. Los objetos 2 y 3 no pueden ir juntos
modelo.add(x[2] + x[3] <= 1)

# 3e. Al menos 2 de los ultimos 4 (objetos 4,5,6,7)
modelo.add(x[4] + x[5] + x[6] + x[7] >= 2)

# 4. Solver: primero buscar TODAS las soluciones factibles (sin optimizar)
solver = cp.CpSolver()
callback = PrintSolutions(x)
status = solver.SearchForAllSolutions(modelo, callback)

print(f"\nEstado del solver (todas las factibles): {solver.status_name(status)}")
print(f"Total de soluciones factibles encontradas: {callback.count}")

# 5. Ahora agregamos el objetivo y resolvemos la optima
valor_total = sum(x[i] * valores[i] for i in range(8))
modelo.Maximize(valor_total)

print(f"\n{'='*50}")
print("RESOLVIENDO CON MAXIMIZACION DEL VALOR...")
status_opt = solver.solve(modelo)
if status_opt == cp.OPTIMAL or status_opt == cp.FEASIBLE:
    seleccionados = [i for i in range(8) if solver.value(x[i]) == 1]
    peso_total = sum(pesos[i] for i in seleccionados)

    print(f"\nSOLUCION OPTIMA")
    print(f"  Objetos seleccionados: {seleccionados}")
    print(f"  Peso total: {peso_total} / {capacidad}")
    print(f"  Valor total optimo: {solver.objective_value}")
    print(f"  Estado: {solver.status_name(status_opt)}")
    print(f"{'='*50}")
else:
    print("No se encontro solucion optima.")
