"""
GUIA: new_int_var() y .only_enforce_if() en OR-Tools CP-SAT

Este archivo explica con ejemplos ejecutables como funcionan y cuando usar
los dos metodos que mas cuestan entender.


PARTE 1: new_int_var(lb, ub, name)
====================================

Crea una variable entera cuyo valor estara en el rango [lb, ub].
El solver elegira un valor dentro de ese rango que cumpla todas las
restricciones.

CASOS DE USO:

  Caso A: Variable con dominio "abierto"
    x = modelo.new_int_var(0, 1000, 'x')
    El solver puede asignar cualquier valor entre 0 y 1000.

  Caso B: Variable con dominio restringido
    s = modelo.new_int_var(1, 9, 's')
    La variable solo puede tomar valores del 1 al 9.
    Esto YA es una restriccion (no hace falta poner model.add(s >= 1)).

  Caso C: Variable FIJA (constante disfrazada)
    c = modelo.new_int_var(5, 5, 'c')
    lb == ub, por lo tanto la variable siempre vale 5.
    Util cuando tienes una matriz con valores conocidos y desconocidos
    (como en el examen de la piramide).

  Caso D: Booleano como new_int_var vs new_bool_var
    b1 = modelo.new_int_var(0, 1, 'b1')   # Entero 0 o 1
    b2 = modelo.new_bool_var('b2')         # Booleano (equivalente a new_int_var(0,1))
    Son casi identicos. La diferencia:
      - b2.Not() existe (niega el booleano) y se usa con .only_enforce_if()
      - b1 NO tiene .Not()
    Regla: si necesitas .only_enforce_if(), usa new_bool_var().


PARTE 2: .only_enforce_if(condicion)
======================================

Hace que una restriccion sea CONDICIONAL. Solo se activa si la condicion
(una variable booleana) es verdadera.

Sintaxis:
    modelo.add(restriccion).only_enforce_if(variable_bool)

Significado:
    SI variable_bool == True  =>  la restriccion DEBE cumplirse
    SI variable_bool == False =>  la restriccion se IGNORA (no aplica)

El 90% de los usos siguen este patron de 3 lineas:
    b = modelo.new_bool_var('b')
    modelo.add(opcion_A).only_enforce_if(b)       # si b=True, se cumple opcion_A
    modelo.add(opcion_B).only_enforce_if(b.Not())  # si b=False, se cumple opcion_B

Esto equivale a decir: "o se cumple opcion_A, o se cumple opcion_B".


CASOS DE USO CONCRETOS:

  Caso 1: Diferencia absoluta |a - b| = k
    Queremos que la diferencia entre a y b sea exactamente k, sin saber
    cual de los dos es mayor. Hay dos posibilidades: a-b=k o b-a=k.

    b = modelo.new_bool_var('b')
    modelo.add(a - b == k).only_enforce_if(b)       # rama 1: a es mayor
    modelo.add(b - a == k).only_enforce_if(b.Not())  # rama 2: b es mayor

    NOTA: OR-Tools tiene AddAbsEquality() que hace esto internamente
    y es mas limpio. Pero en el examen puede que pidan hacerlo manual.

  Caso 2: Division sin saber orden (max/min = k)
    Ejemplo del KenKen: max(a,b) / min(a,b) = k
    Hay dos casos: a es el mayor (a = k*b) o b es el mayor (b = k*a).

    b = modelo.new_bool_var('b')
    modelo.add(a == k * b).only_enforce_if(b)        # a es k veces b
    modelo.add(b == k * a).only_enforce_if(b.Not())   # b es k veces a

  Caso 3: Implicacion "si X entonces Y"
    "Si el objeto 0 esta seleccionado, entonces el objeto 1 tambien"
    Esto NO necesita .only_enforce_if() si es una implicacion simple.
    Se modela como: x[0] <= x[1]  (si x[0]=1, fuerza x[1]=1)

    Pero si es mas complejo:
    "Si x == 5 entonces y debe ser par"
    Aqui si necesitas .only_enforce_if():
        cond = modelo.new_bool_var('cond')
        modelo.add(x == 5).only_enforce_if(cond)
        modelo.add(y % 2 == 0).only_enforce_if(cond)
    Aunque este caso es raro en examenes.

  Caso 4: "Exactamente una de estas N opciones debe cumplirse"
    Similar al caso 1 pero con multiples ramas. Necesitas N booleanos
    y forzar que exactamente uno sea True.
    Ejemplo: si una variable debe ser 2, 5 o 7:
        b2 = modelo.new_bool_var('b2')
        b5 = modelo.new_bool_var('b5')
        b7 = modelo.new_bool_var('b7')
        modelo.add(x == 2).only_enforce_if(b2)
        modelo.add(x == 5).only_enforce_if(b5)
        modelo.add(x == 7).only_enforce_if(b7)
        modelo.add(b2 + b5 + b7 == 1)  # exactamente una activa


RESUMEN RAPIDO PARA EL EXAMEN:
===============================

  new_int_var(lb, ub, name):
    - Si los valores son fijos (conocidos), usa lb=ub.
    - Si es booleano y necesitas .Not(), usa new_bool_var().
    - Si es booleano y NO necesitas .Not(), new_int_var(0,1) tambien sirve.

  .only_enforce_if():
    - SOLO se usa cuando una restriccion debe ser CONDICIONAL.
    - Patron tipico: creas un bool, activas opcion A con el bool,
      activas opcion B con bool.Not().
    - Si la restriccion siempre debe cumplirse, NO uses .only_enforce_if(),
      usa model.add(restriccion) a secas.
    - Para diferencia absoluta simple, AddAbsEquality() es mas facil.


EJEMPLOS EJECUTABLES A CONTINUACION:
=====================================
"""

from ortools.sat.python import cp_model as cp

print("=" * 60)
print("EJEMPLO 1: new_int_var() — los 4 casos")
print("=" * 60)

modelo = cp.CpModel()

# Caso A: dominio abierto
x = modelo.new_int_var(0, 100, 'x')

# Caso B: dominio restringido (no hace falta add(x>=1) ni add(x<=9))
digito = modelo.new_int_var(1, 9, 'digito')

# Caso C: variable FIJA (constante). Siempre valdra 5.
fijo = modelo.new_int_var(5, 5, 'fijo')

# Caso D: new_bool_var vs new_int_var(0,1)
b1 = modelo.new_int_var(0, 1, 'b_entero')
b2 = modelo.new_bool_var('b_bool')

# Restricciones de prueba
modelo.add(x == digito + fijo)       # x = digito + 5
modelo.add(digito >= 3)               # el digito es al menos 3
modelo.add(b1 == 1)                   # forzamos ambos booleanos a 1
modelo.add(b2 == 1)

solver = cp.CpSolver()
status = solver.solve(modelo)
if status == cp.OPTIMAL or status == cp.FEASIBLE:
    print(f"x      = {solver.value(x)}       (dominio 0..100)")
    print(f"digito = {solver.value(digito)}  (dominio 1..9, restringido a >=3)")
    print(f"fijo   = {solver.value(fijo)}    (siempre 5)")
    print(f"b1     = {solver.value(b1)}      (new_int_var(0,1))")
    print(f"b2     = {solver.value(b2)}      (new_bool_var)")
    print(f"\nb2.Not() existe? Si. b1.Not()? No — por eso new_bool_var es mejor")
    print(f"para usar con .only_enforce_if()")


print("\n" + "=" * 60)
print("EJEMPLO 2: .only_enforce_if() — Diferencia absoluta manual")
print("=" * 60)

modelo2 = cp.CpModel()
a = modelo2.new_int_var(0, 10, 'a')
b = modelo2.new_int_var(0, 10, 'b')

# Queremos: |a - b| = 4  (la diferencia entre a y b es 4)
# Hay 2 posibilidades: a-b=4 o b-a=4
rama = modelo2.new_bool_var('rama')
modelo2.add(a - b == 4).only_enforce_if(rama)        # Si rama=True  => a es mayor
modelo2.add(b - a == 4).only_enforce_if(rama.Not())  # Si rama=False => b es mayor

# Forzamos valores para ver ambas ramas
modelo2.add(a == 7)

solver2 = cp.CpSolver()
status2 = solver2.solve(modelo2)
if status2 == cp.OPTIMAL or status2 == cp.FEASIBLE:
    print(f"a = {solver2.value(a)}, b = {solver2.value(b)}")
    print(f"|a - b| = {abs(solver2.value(a) - solver2.value(b))}")
    print(f"rama = {solver2.value(rama)}")
    print(f"\nInterpretacion:")
    if solver2.value(rama):
        print(f"  rama=True  => se activo a-b=4 => {solver2.value(a)}-{solver2.value(b)}=4")
    else:
        print(f"  rama=False => se activo b-a=4 => {solver2.value(b)}-{solver2.value(a)}=4")
    print(f"  La otra rama se IGNORO (no se forzo).")


print("\n" + "=" * 60)
print("EJEMPLO 3: .only_enforce_if() — Division sin saber el orden")
print("=" * 60)

modelo3 = cp.CpModel()
p = modelo3.new_int_var(1, 6, 'p')
q = modelo3.new_int_var(1, 6, 'q')

# Queremos: max(p,q) / min(p,q) = 2
# Si p es el mayor: p = 2*q
# Si q es el mayor: q = 2*p
orden = modelo3.new_bool_var('orden')
modelo3.add(p == 2 * q).only_enforce_if(orden)        # p es el doble de q
modelo3.add(q == 2 * p).only_enforce_if(orden.Not())  # q es el doble de p

# Forzamos p=4 para ver que q se ve obligado a ser 2
modelo3.add(p == 4)

solver3 = cp.CpSolver()
status3 = solver3.solve(modelo3)
if status3 == cp.OPTIMAL or status3 == cp.FEASIBLE:
    print(f"p = {solver3.value(p)}, q = {solver3.value(q)}")
    max_val = max(solver3.value(p), solver3.value(q))
    min_val = min(solver3.value(p), solver3.value(q))
    print(f"max/min = {max_val}/{min_val} = {max_val/min_val}")
    print(f"orden = {solver3.value(orden)}")
    print(f"\nInterpretacion:")
    if solver3.value(orden):
        print(f"  orden=True  => p es el mayor => p=2*q")
    else:
        print(f"  orden=False => q es el mayor => q=2*p")


print("\n" + "=" * 60)
print("EJEMPLO 4: .only_enforce_if() — Variable que debe ser 2, 5 o 7")
print("=" * 60)

modelo4 = cp.CpModel()
v = modelo4.new_int_var(0, 10, 'v')

# v solo puede ser 2, 5 o 7
b2 = modelo4.new_bool_var('es_2')
b5 = modelo4.new_bool_var('es_5')
b7 = modelo4.new_bool_var('es_7')

modelo4.add(v == 2).only_enforce_if(b2)
modelo4.add(v == 5).only_enforce_if(b5)
modelo4.add(v == 7).only_enforce_if(b7)
modelo4.add(b2 + b5 + b7 == 1)  # exactamente una opcion activa

solver4 = cp.CpSolver()
status4 = solver4.solve(modelo4)
if status4 == cp.OPTIMAL or status4 == cp.FEASIBLE:
    print(f"v = {solver4.value(v)}")
    print(f"es_2={solver4.value(b2)}, es_5={solver4.value(b5)}, es_7={solver4.value(b7)}")
    print(f"\nInterpretacion:")
    print(f"  Solo una de las 3 restricciones .only_enforce_if() se activo.")
    print(f"  Las otras 2 se ignoraron. v tomo el valor de la activa.")


print("\n" + "=" * 60)
print("EJEMPLO 5: CUANDO NO usar .only_enforce_if()")
print("=" * 60)

print("""
ERROR COMUN: poner .only_enforce_if() en restricciones que SIEMPRE
deben cumplirse.

  MAL:
    modelo.add(x + y == 10).only_enforce_if(b)  # Si b=False, la suma NO se fuerza

  BIEN:
    modelo.add(x + y == 10)  # La suma siempre debe ser 10

  MAL (para implicacion simple x=1 => y=1):
    modelo.add(y == 1).only_enforce_if(x == 1)  # MUY MAL, x==1 no es bool var

  BIEN (equivalente matematico):
    modelo.add(y >= x)  # Si x=1, fuerza y>=1 (y como es bool, y=1)

.only_enforce_if() SOLO se usa cuando realmente necesitas que una
restriccion sea OPCIONAL (se active o no segun una variable booleana).
""")

print("=" * 60)
print("FIN DE LA GUIA")
print("=" * 60)
