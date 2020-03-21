import LinearOptimization as LO
import numpy as np

A = np.array([[2,1,8],[1,2,10],[30,50,0]])

# print(A)
# print("________________________________")
# print(np.delete(A,2,axis=1))



test = LO.Optimizer(A,primal_independent=["*x1","x2"],primal_dependent=["0","t2"])




test.simplex_algorithm()
