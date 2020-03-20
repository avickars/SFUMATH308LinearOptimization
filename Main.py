import LinearOptimization as LO
import numpy as np
import pprint

A = np.array([[-1, -2, -3], [3, -4, -3], [5, 6, 3],[5,6,7]])
m = 4
n = 3
test = LO.Optimizer(A)
# test.print()



test.simplex_algorithm()
