import LinearOptimization as LO
import numpy as np

A = np.array([[1,4,-7],[3,4,8],[5,6,0]])

example = LO.Optimizer(A)

example.simplex_algorithm()
