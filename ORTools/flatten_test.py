import numpy as np

matriz = [[1,2,3],[4,5,6],[7,8,9]]

m = np.array(matriz)

for fila in range(m.shape[0]):
    for columna in range(m.shape[1]):
        print(m[fila][columna], end=" ")
    print()
print()

flat = m.flatten()
for i,j in ((0,3), (6,9)):
    print(flat[i:j:1], end=" ")