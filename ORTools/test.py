import numpy as np
import builtins

matriz = [[f"({r},{c})" for r in range(4)] for c in range(4)] 

matriz_np = np.array(matriz)
print(matriz_np.flatten())

