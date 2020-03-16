import numpy as np

class Optimizer:
    def __init__(self, T, m, n, p):
        self.T = np.array(T)
        self.n = n
        self.m = m
        self.primal = p
        self.pivot_order = p

    def print(self):
        print("T = ")
        for i in self.T:
            print(i)
        print("m = ", self.m)
        print("n = ", self.n)

    def simplex_algorithm(self):
        while any(self.T[0:self.m, self.n - 1] < 0):  # Testing for Maximum Basic Feasible Tableau
            self.maximum_basic_feasible()
            break

    def maximum_basic_feasible(self):
        for i in reversed(range(0,self.m-1)):
            if self.T[i,self.m-1] < 0:
                if all(self.T[i,0:self.m-1] >= 0):
                    print("Unbounded in Row:", i)
                    print(self.T)
                else:
                    pivot_columns = np.where(self.T[i,self.m-1] < 0)[0]
                    print(self.blands_anti_cycling(pivot_columns))

    def blands_anti_cycling(self, pivots):
        if len(pivots) == 1:
            return pivots[0]
        else:
            print("fds")










