import numpy as np


class Optimizer:
    def __init__(self, A, primal_independent = [], primal_dependent = []):
        self.A = np.array(A)  # Tableau A
        self.n = len(A[0,:])  # Number of Columns
        self.m = len(A[:,0])  # Number of Rows

        if primal_independent != [] and primal_dependent !=[]:  # Both Independent and Dependent Vars are specified in the class call
            self.primal_ind = primal_independent
            self.primal_dep = primal_dependent
        elif primal_independent == [] and primal_dependent == []: # Both Independent and Dependent Vars are not specified in the class call
            self.primal_ind = self.variable_creator("x", self.n)
            self.primal_dep = self.variable_creator("t", self.m)
        elif not primal_independent:  # Only Dependent Vars are specified in the class call
            self.primal_ind = self.variable_creator("x", self.n)
            self.primal_dep = primal_dependent
        elif not primal_independent:  # Only Independent Vars are specified in the class call
            self.primal_ind = primal_independent
            self.primal_dep = self.variable_creator("t", self.m)

        self.blands_rule = self.primal_ind + self.primal_dep  # Initializes Variable Order for Blands Anti Cycling Rule

    def variable_creator(self, var, iterable):
        variables = [var] * iterable
        for j in range(0, iterable):
            variables[j] = var + str(j + 1)
        return variables

    def print(self):
        print("T = ", self.A)
        print("m = ", self.m)
        print("n = ", self.n)
        print("Independent Variables: ", self.primal_ind)
        print("Dependent Variables: ", self.primal_dep)
        print("Blands Rule: ", self.blands_rule)

    def simplex_algorithm(self):
        while any(self.A[0:self.m,self.n-1] < 0): # Testing if the Tableau is Maximum Basic Feasible
            print("here")
            if not self.max_basic_feasible():
                break
            break  # *****************************Controlling Loop ----- REMOVE LATER

    def max_basic_feasible(self):
        # loop from the bottom up, testing to see if any b_i<0.
        for i in reversed(range(0,self.m)):
            if self.A[i,self.n-1] < 0:
                if not self.infeasible_check(i):
                    return False
                print("pivot here")
                possible_pivot_columns = np.where(self.A[i,0:self.n-1] < 0)
                if len(possible_pivot_columns) > 1:  # If there are more than one choice, this will pass to method to decide which one
                    pivot = self.which_pivot_to_use([self.primal_ind[i] for i in possible_pivot_columns[0]]) #****************************** CONTINUE HERE TO CODE PIVOT

        return True # Returns True if the Tableau is now Maximum Basic Feasible

    def which_pivot_to_use(self, choices):  # Returns the Proper Choice According to the Order for Blands Anti Cycling Rule
        for bland in self.blands_rule:
            if bland in choices:
                print(bland)
                return bland

    def infeasible_check(self, i):
        # This method checks if given a row of the tableau with b_i<0, it will test if the other the entries in the row are neg/pos and return false if they are indicating
        # that the tableau is infeasible
        if all(self.A[i, 0:self.n - 1] <= 0):
            print("Tableau is Infeasible! No Solution!")
            return False
        else:
            return True



