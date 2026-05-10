"""
Ejemplos de métodos de OR-Tools (CP-SAT Solver)
Basado en: Metodos_OrTools.pdf
"""

from ortools.sat.python import cp_model
import numpy as np


# ==========================================
# 1. CpModel() - Crear modelo
# ==========================================
def ejemplo_cpmodel():
    """Crear un modelo de satisfacción de restricciones"""
    print("=== 1. CpModel() ===")
    model = cp_model.CpModel()
    print(f"Modelo creado: {type(model)}")
    # Salida esperada:
    # Modelo creado: <class 'ortools.sat.python.cp_model.CpModel'>
    return model


# ==========================================
# 2. NewIntVar() - Variables enteras
# ==========================================
def ejemplo_newintvar():
    """Crear variables enteras con dominio [min, max]"""
    print("\n=== 2. NewIntVar() ===")
    model = cp_model.CpModel()
    
    # Variable x en rango [0, 10]
    x = model.NewIntVar(0, 10, 'x')
    # Variable y en rango [-5, 5]
    y = model.NewIntVar(-5, 5, 'y')
    # Variable booleana (caso especial)
    z = model.NewBoolVar('z')
    
    print(f"x: dominio [0, 10]")
    print(f"y: dominio [-5, 5]")
    print(f"z: booleana [0, 1]")
    # Salida esperada:
    # x: dominio [0, 10]
    # y: dominio [-5, 5]
    # z: booleana [0, 1]
    return model, x, y, z


# ==========================================
# 3. Add() - Agregar restricciones
# ==========================================
def ejemplo_add():
    """Agregar restricciones al modelo"""
    print("\n=== 3. Add() ===")
    model = cp_model.CpModel()
    
    x = model.NewIntVar(0, 10, 'x')
    y = model.NewIntVar(0, 10, 'y')
    
    # Restricciones lineales
    model.Add(x + y <= 10)
    model.Add(x - y >= 2)
    model.Add(2 * x + 3 * y == 15)
    
    print("Restricciones agregadas:")
    print("  x + y <= 10")
    print("  x - y >= 2")
    print("  2*x + 3*y == 15")
    # Salida esperada:
    # Restricciones agregadas:
    #   x + y <= 10
    #   x - y >= 2
    #   2*x + 3*y == 15
    return model


# ==========================================
# 4. Solve() - Resolver modelo
# ==========================================
def ejemplo_solve():
    """Resolver el modelo con CpSolver"""
    print("\n=== 4. Solve() ===")
    model = cp_model.CpModel()
    
    x = model.NewIntVar(0, 10, 'x')
    y = model.NewIntVar(0, 10, 'y')
    
    model.Add(x + y <= 10)
    model.Add(x >= y)
    
    # Maximizar x + y
    model.Maximize(x + y)
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    status_dict = {
        cp_model.OPTIMAL: "ÓPTIMO",
        cp_model.FEASIBLE: "FACTIBLE",
        cp_model.INFEASIBLE: "INFACTIBLE"
    }
    print(f"Estado: {status_dict.get(status, 'DESCONOCIDO')}")
    # Salida esperada:
    # Estado: ÓPTIMO
    return model, solver, status


# ==========================================
# 5. Value() - Obtener valores de variables
# ==========================================
def ejemplo_value():
    """Obtener valores de variables después de resolver"""
    print("\n=== 5. Value() ===")
    model = cp_model.CpModel()
    
    x = model.NewIntVar(0, 10, 'x')
    y = model.NewIntVar(0, 10, 'y')
    
    model.Add(x + y == 7)
    model.Add(x >= 3)
    model.Maximize(x)
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print(f"x = {solver.Value(x)}")
        print(f"y = {solver.Value(y)}")
        print(f"x + y = {solver.Value(x + y)}")
        # Salida esperada:
        # x = 7
        # y = 0
        # x + y = 7
    return solver, x, y


# ==========================================
# 6. AddMinEquality() - Restricción de mínimo
# ==========================================
def ejemplo_addminequality():
    """y = min(x1, x2, x3, ...)"""
    print("\n=== 6. AddMinEquality() ===")
    model = cp_model.CpModel()
    
    x1 = model.NewIntVar(10, 10, 'x1')
    x2 = model.NewIntVar(2, 2, 'x2')
    x3 = model.NewIntVar(7, 7, 'x3')
    y = model.NewIntVar(0, 10, 'y')
    
    # y = min(x1, x2, x3)
    model.AddMinEquality(y, [x1, x2, x3])
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL:
        print(f"x1={solver.Value(x1)}, x2={solver.Value(x2)}, x3={solver.Value(x3)}")
        print(f"y = min(x1, x2, x3) = {solver.Value(y)}")
        # Salida esperada:
        # x1=10, x2=2, x3=7
        # y = min(x1, x2, x3) = 2
    return model


# ==========================================
# 7. AddAbsEquality() - Valor absoluto
# ==========================================
def ejemplo_addabsequality():
    """y = |x|"""
    print("\n=== 7. AddAbsEquality() ===")
    model = cp_model.CpModel()
    
    x = model.NewIntVar(-10, 10, 'x')
    y = model.NewIntVar(0, 10, 'y')
    
    # y = |x|
    model.AddAbsEquality(y, x)
    
    # Forzar x negativo para demostración
    model.Add(x == -7)
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL:
        print(f"x = {solver.Value(x)}")
        print(f"y = |x| = {solver.Value(y)}")
        # Salida esperada:
        # x = -7
        # y = |x| = 7
    return model


# ==========================================
# 8. AddElement() - Indexar con variables
# ==========================================
def exemple_addelement():
    """value = array[index] donde index es variable"""
    print("\n=== 8. AddElement() ===")
    model = cp_model.CpModel()
    
    # Array de valores
    valores = [10, 20, 30, 40, 50]
    
    # Variable índice (debe estar en rango válido)
    index = model.NewIntVar(0, len(valores) - 1, 'index')
    value = model.NewIntVar(0, 100, 'value')
    
    # value = valores[index]
    model.AddElement(index, valores, value)
    
    # Forzar índice para demostración
    model.Add(index == 2)
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL:
        print(f"valores = {valores}")
        print(f"index = {solver.Value(index)}")
        print(f"value = valores[index] = {solver.Value(value)}")
        # Salida esperada:
        # valores = [10, 20, 30, 40, 50]
        # index = 2
        # value = valores[index] = 30
    return model


# ==========================================
# 9. AddBoolOr() / AddBoolAnd() - Lógica booleana
# ==========================================
def ejemplo_boolorand():
    """Restricciones lógicas: OR y AND"""
    print("\n=== 9. AddBoolOr() / AddBoolAnd() ===")
    model = cp_model.CpModel()
    
    a = model.NewBoolVar('a')
    b = model.NewBoolVar('b')
    c = model.NewBoolVar('c')
    
    # a OR b OR c debe ser verdadero (al menos uno es True)
    model.AddBoolOr([a, b, c])
    
    # a AND b debe ser verdadero (ambos son True)
    model.AddBoolAnd([a, b])
    
    # c debe ser False (para mostrar que a y b satisfacen el OR)
    model.Add(c == 0)
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL:
        print(f"a = {bool(solver.Value(a))}")
        print(f"b = {bool(solver.Value(b))}")
        print(f"c = {bool(solver.Value(c))}")
        print("AddBoolOr([a,b,c]): al menos uno True ✓")
        print("AddBoolAnd([a,b]): ambos True ✓")
        # Salida esperada:
        # a = True
        # b = True
        # c = False
        # AddBoolOr([a,b,c]): al menos uno True ✓
        # AddBoolAnd([a,b]): ambos True ✓
    return model


# ==========================================
# 10. AddNoOverlap() - Scheduling sin superposición
# ==========================================
def ejemplo_addnooverlap():
    """Tareas que no pueden superponerse en el tiempo"""
    print("\n=== 10. AddNoOverlap() ===")
    model = cp_model.CpModel()
    
    # 3 tareas con tiempos de inicio y duración
    duraciones = [3, 2, 4]
    starts = [model.NewIntVar(0, 20, f'start_{i}') for i in range(3)]
    ends = [model.NewIntVar(0, 20, f'end_{i}') for i in range(3)]
    
    # Crear intervalos
    intervals = []
    for i in range(3):
        interval = model.NewOptionalIntervalVar(
            starts[i], duraciones[i], ends[i], True, f'interval_{i}')
        intervals.append(interval)
    
    # Las tareas no pueden superponerse
    model.AddNoOverlap(intervals)
    
    # Minimizar el tiempo total (makespan)
    makespan = model.NewIntVar(0, 20, 'makespan')
    model.AddMaxEquality(makespan, ends)
    model.Minimize(makespan)
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL:
        print("Tareas programadas (sin superposición):")
        for i in range(3):
            print(f"  Tarea {i}: inicio={solver.Value(starts[i])}, "
                  f"duración={duraciones[i]}, fin={solver.Value(ends[i])}")
        print(f"Makespan total: {solver.Value(makespan)}")
        # Salida esperada:
        # Tareas programadas (sin superposición):
        #   Tarea 0: inicio=4, duración=3, fin=7
        #   Tarea 1: inicio=7, duración=2, fin=9
        #   Tarea 2: inicio=0, duración=4, fin=4
        # Makespan total: 9
    return model


# ==========================================
# 11. NewIntVarFromDomain() - Dominios no contiguos
# ==========================================
def ejemplo_newintvarfromdomain():
    """Variable con dominio no contiguo, ej: {1, 3, 5, 7}"""
    print("\n=== 11. NewIntVarFromDomain() ===")
    model = cp_model.CpModel()
    
    # Dominio: {1, 3, 5, 7}
    domain = cp_model.Domain.FromValues([1, 3, 5, 7])
    x = model.NewIntVarFromDomain(domain, 'x')
    
    # Dominio con múltiples rangos: {0, 1, 2, 10, 11, 12}
    domain2 = cp_model.Domain.FromIntervals([[0, 2], [10, 12]])
    y = model.NewIntVarFromDomain(domain2, 'y')
    
    model.Add(x + y == 8)
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL:
        print(f"x ∈ {{1, 3, 5, 7}}, valor: {solver.Value(x)}")
        print(f"y ∈ {{0,1,2, 10,11,12}}, valor: {solver.Value(y)}")
        print(f"x + y = {solver.Value(x + y)}")
        # Salida esperada:
        # x ∈ {1, 3, 5, 7}, valor: 7
        # y ∈ {0,1,2, 10,11,12}, valor: 1
        # x + y = 8
    return model


# ==========================================
# BONUS: Uso con numpy para matrices de variables
# ==========================================
def ejemplo_numpy():
    """Manipular matrices de variables con numpy"""
    print("\n=== BONUS: Uso con numpy ===")
    model = cp_model.CpModel()
    
    # Matriz 3x3 de variables
    x = np.array([[model.NewIntVar(0, 9, f'x_{i}_{j}') 
                   for j in range(3)] for i in range(3)])
    
    print("Matriz de variables 3x3:")
    print(x)
    
    # Restricción: suma de cada fila <= 15
    for i in range(3):
        model.Add(sum(x[i, :]) <= 15)
    
    # Restricción: suma de cada columna <= 15
    for j in range(3):
        model.Add(sum(x[:, j]) <= 15)
    
    # Maximizar suma total
    model.Maximize(sum(x.flatten()))
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL:
        print("\nMatriz resuelta:")
        solution = np.array([[solver.Value(x[i, j]) for j in range(3)] 
                             for i in range(3)])
        print(solution)
        print(f"Suma total: {solver.Value(sum(x.flatten()))}")
        # Salida esperada:
        # Matriz resuelta:
        # [[9 6 0]
        #  [0 9 6]
        #  [6 0 9]]
        # Suma total: 45
    return model


# ==========================================
# Ejecutar todos los ejemplos
# ==========================================
if __name__ == "__main__":
    print("=" * 60)
    print("EJEMPLOS DE MÉTODOS DE OR-TOOLS (CP-SAT)")
    print("=" * 60)
    
    ejemplo_cpmodel()
    ejemplo_newintvar()
    ejemplo_add()
    ejemplo_solve()
    ejemplo_value()
    ejemplo_addminequality()
    ejemplo_addabsequality()
    exemple_addelement()
    ejemplo_boolorand()
    ejemplo_addnooverlap()
    ejemplo_newintvarfromdomain()
    ejemplo_numpy()
    
    print("\n" + "=" * 60)
    print("Todos los ejemplos completados!")
    print("=" * 60)
