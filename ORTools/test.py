import numpy as np

matriz_m = [[f"{r}_{c}" for c in range(4)] for r in range(4)]
matriz = np.array(matriz_m)

matriz_d = matriz.diagonal()
lista = [valor for valor in matriz_d.tolist()]
print(lista)