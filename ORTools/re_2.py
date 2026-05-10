import numpy 

lst = [(r,c) for r in range(3) for c in range(3)]
print(lst)

matriz = [[1,2,3],
          [4,5,6],
          [7,8,9]]
for i in range(len(matriz)):
    for j in range(len(matriz[i])):
        print(f"Elemento de la matriz {matriz[i][j]} y posicion {i}{j}")

for i in matriz:
    for j in i:
        print(f"Elemeto de la matriz2 {j}")
print()


# Con numpy
np = numpy.array(matriz)
print(np.diagonal())
print()

print(np[:, 1:])