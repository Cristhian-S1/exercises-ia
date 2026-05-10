import numpy as np
import builtins

matriz = [[f"({r},{c})" for r in range(4)] for c in range(4)] 

matriz_np = np.array(matriz)
matriz_np_tp = matriz_np.transpose()

print(matriz_np, "\n")
print(matriz_np_tp)

print(sum([1,2,3]))

