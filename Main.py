import LinearOptimization as LO
import numpy as np

A = np.array([[0,2,10],[3,1,15],[1,3,0]])

test = LO.Optimizer(A, primal_independent=["*x", "y"], primal_dependent=["0","t2"])

test.simplex_algorithm()
