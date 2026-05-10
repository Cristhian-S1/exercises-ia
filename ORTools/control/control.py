from ortools.sat.python import cp_model as cp
import numpy as np

#1. Declarar el model mediente la clase CpModel()
modelo = cp.CpModel()

#2. Declarar el dominio y variables

#Piramide de 7 niveles
piramide = [
            [717],
            [-1,-1],
            [168,-1,203],
            [-1,-1,-1,-1],
            [56,-1,40,-1,49],
            [-1,-1,-1,-1,-1,-1],
            [16,-1,4,-1,16,-1,3]
        ]

matriz = [ 
    [
    modelo.new_int_var(valor, valor, f'value_{nivel}') if valor != -1 else 
    modelo.new_int_var(0, 1000, f"value_{nivel}")
    for valor in nivel
    ] for nivel in piramide ]


#3. Restricciones 
for nivel in range(len(matriz)-1, 0, -1):
    #print(matriz[nivel])
    for col in range(len(matriz[nivel])-1):
        modelo.add(matriz[nivel][col] + matriz[nivel][col+1] == matriz[nivel-1][col])
        #print(matriz[nivel][col], end=' ')
    print()
    
#4. Solver
solver = cp.CpSolver()
status = solver.solve(modelo)

if status == cp.OPTIMAL or status == cp.FEASIBLE:
    for fila in matriz:
        print()
        for numero in fila:
            print(f"numero = {solver.value(numero)}")
    print()
else:
    print("Solucion no encontrada")


"""
for nivel in range(len(piramide)-1, 0, -1):
    print(piramide[nivel])
    for col in range(len(piramide[nivel])-1):
        #piramide[nivel][col], piramide[nivel][col+1], piramide[nivel-1][col]
        print(piramide[nivel][col], end=' ')
    print()
"""