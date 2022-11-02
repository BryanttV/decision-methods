import numpy as np

mat = np.empty([3, 3])

print(mat)

mat.fill(1)

mat[0,:] = [1,2,"hola"]

print(mat)