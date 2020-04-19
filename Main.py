import LinearOptimization as LO
import numpy as np

A = np.array([[-2, 1, -2], [1, -1, -1], [1, 1, 0]])

example = LO.Optimizer(A, primal_independent=["*x", "y", "z"], primal_dependent=["0", "t"])

example.simplex_algorithm()
