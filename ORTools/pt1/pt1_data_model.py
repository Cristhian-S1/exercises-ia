"""
Efectivamente, sucede exactamente lo mismo que con `add()`. La instancia `model` (que es un objeto de la clase `CpModel`)
 actúa como un **contenedor central** que va acumulando toda la definición del problema.

Aquí te explico cómo lo gestiona internamente:

### 1. El "Protocol Buffer" (El almacén interno)
Por debajo, la clase `CpModel` de Python maneja un objeto llamado `CpModelProto`. 
Este es un formato de mensajería de Google (Protocol Buffers) que sirve para comunicar tu código Python
con el motor de resolución escrito en C++.

Cuando ejecutas `model.new_int_var(0, 2, "x")`:
1. El modelo crea una nueva entrada en una **lista interna de variables** dentro de ese "Proto".
2. Guarda el **nombre** ("x"), el **límite inferior** (0) y el **límite superior** (2).
3. Le asigna un **índice** (0, 1, 2, etc.) según el orden en que las creas.

### 2. ¿Qué es entonces el objeto `x`?
La variable `x` que recibes en Python no contiene los datos de la variable, 
sino que es un objeto de tipo `IntVar` que guarda una referencia (el índice) al modelo. 
Es como un "puntero" o un acceso directo a esa posición en la lista interna del modelo.

### 3. Diferencia con `add()`
La diferencia es mínima y solo estructural:
* **`new_int_var()`**: Alimenta una lista llamada `variables` dentro del modelo.
* **`add()`**: Alimenta una lista llamada `constraints` dentro del modelo.

### ¿Por qué es importante esto?
Es la razón por la cual **no puedes mezclar variables de dos modelos distintos**. Si intentas hacer esto:

```python
model_a = cp_model.CpModel()
model_b = cp_model.CpModel()

x = model_a.new_int_var(0, 2, "x")
model_b.add(x == 1) # <--- ERROR
```

El `model_b` dará un error porque buscará la variable con el índice de `x` en su propia lista interna y
o no existirá, o será una variable completamente diferente que pertenece a `model_b`.

**En resumen:** Sí, la instancia `model` es la dueña de todas las variables y restricciones
y las mantiene organizadas en listas internas para que, cuando llames a `solver.solve(model)`,
pueda enviarle el "paquete" completo de datos al motor de búsqueda.
"""