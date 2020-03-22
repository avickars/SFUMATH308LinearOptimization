import LinearOptimization as LO
import numpy as np

A = np.array([[2, 1, 8,5], [1, 2, 10,5], [-30, 50, 0,5],[-30,-50,-30,-50]])



test = LO.Optimizer(A, primal_independent=["*x1", "x2","*x3"], primal_dependent=["t1", "0","t3"])

test.simplex_algorithm()
