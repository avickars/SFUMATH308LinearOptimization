import LinearOptimization as LO
import numpy as np

A = np.array([[1, -2, -3], [3, -4, 3], [5, 6, 3]])

# print(A[1,:]<0)

test = LO.Optimizer(A, 3, 3, ['x1', 'x2', 't1', 't2'])

test.simplex_algorithm()
