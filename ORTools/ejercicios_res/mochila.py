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
"""

from ortools.sat.python import cp_model as cp
import numpy as np

#1. Declarar instancia del CpModel()
modelo = cp.CpModel()

#2. Declarar estructura
pesos = [4,3,5,2,6,1,3,2]
valores = [10,6,12,5,15,3,7,4]

objetos = [modelo.new_int_bool(f"{i}") for i in range(8)]

# Restriccion de peso
modelo.add( sum(pesos[i]* objetos[i] for i in range(len(pesos)) <= 14 ))

#Si escoje objeto 0, tambien 1, si vale 1 el objetos[0] si o si el objetos[1] vale 1
modelo.add(objetos[0] <= objetos[1])

#Objetos 2 y 3 no pueden seleccionarse simultaneamente
modelo.add(objetos[2] + objetos[3] <= 1)

#Seleccionar entre 3 y 5 objetos en total
modelo.add(sum(objetos) >= 3)
modelo.add(sum(objetos) <= 5)

#Al menos 2 objetos de entre los ultimos 4
modelo.add( sum(objetos[i] for i in [4,5,6,7]) >= 2)

modelo.maximize(sum(valores[i]*objetos for i in range(len(pesos))))

