import LinearOptimization as LO
import numpy as np

A = np.array([[1,2,10],[3,1,15],[1,3,0]])


test = LO.Optimizer(A, primal_independent=["*x", "*y"], primal_dependent=["t1","t2"])

test.simplex_algorithm()
