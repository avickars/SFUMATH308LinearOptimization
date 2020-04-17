import LinearOptimization as LO
import numpy as np

A = np.array([[-2,0,-1,0],[-1,1,0,-1],[3,-1,1,3],[5,-1,2,0]])

test = LO.Optimizer(A, primal_independent=["*x", "*y", "*z"], primal_dependent=["0", "s2","s3"])

test.simplex_algorithm()
