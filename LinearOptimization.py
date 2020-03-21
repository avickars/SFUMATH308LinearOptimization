import numpy as np
from fractions import Fraction


class Optimizer:
    def __init__(self, A, primal_independent=[], primal_dependent=[]):
        self.A = np.array(A)  # Tableau A
        self.A = self.A.astype('float64')
        self.n = len(A[0, :]) - 1  # Number of Columns
        self.m = len(A[:, 0]) - 1  # Number of Rows

        if primal_independent != [] and primal_dependent != []:  # Both Independent and Dependent Vars are specified in the class call
            self.primal_ind = primal_independent + ["-1"]
            self.primal_dep = primal_dependent + ["f"]
        elif primal_independent == [] and primal_dependent == []:  # Both Independent and Dependent Vars are not specified in the class call
            self.primal_ind = self.variable_creator("x", self.n) + ["-1"]
            self.primal_dep = self.variable_creator("t", self.m) + ["f"]
        elif not primal_independent:  # Only Dependent Vars are specified in the class call
            self.primal_ind = self.variable_creator("x", self.n) + ["-1"]
            self.primal_dep = primal_dependent + ["f"]
        elif not primal_independent:  # Only Independent Vars are specified in the class call
            self.primal_ind = primal_independent + ["-1"]
            self.primal_dep = self.variable_creator("t", self.m) + ["f"]

        self.blands_rule = self.primal_ind + self.primal_dep  # Initializes Variable Order for Blands Anti Cycling Rule

        self.dual_ind = self.dual_variable_creator("y", self.m, True) + ["-1"]
        self.dual_dep = self.dual_variable_creator("s", self.n, False) + ["g"]

    def dual_variable_creator(self,var,iterable,dual_primal):
        variables = [var] * iterable
        for j in range(0, iterable):
            if not dual_primal:
                if self.primal_dep[j].startswith("0"):  # Testing for Equality in the Constraints
                    variables[j] = '0'
                else:
                    variables[j] = var + str(j + 1)
            else:
                if self.primal_dep[j] == '0':  # Testing for Equality in the Constraints
                    variables[j] = '*' + var + str(j + 1)
                else:
                    variables[j] = var + str(j + 1)
        return variables

    def variable_creator(self, var, iterable):
        variables = [var] * iterable
        for j in range(0, iterable):
            variables[j] = var + str(j + 1)
        return variables

    def print(self):
        print("A = ", self.A)
        print("Primal Independent Variables: ", self.primal_ind)
        print("Primal Dependent Variables: ", self.primal_dep)

        print("Dual Independent Variables: ", self.dual_ind)
        print("Dual Dependent Variables: ", self.dual_dep)

    def simplex_algorithm(self):
        self.print()

        print("********************************************************************************************************************************************************")
        print("********************************************************************************************************************************************************")
        while any(self.A[0:self.m, self.n] < 0):  # Testing if the Tableau is Maximum Basic Feasible
            if not self.max_basic_feasible():
                return
        print("The Primal is Maximum Basic Feasible")
        print("********************************************************************************************************************************************************")

        while any(self.A[self.m, 0:self.n] > 0):  # Testing if the Tableau is Optimal
            if not self.optimal():
                return
        print("********************************************************************************************************************************************************")
        print("********************************************************************************************************************************************************")
        self.final_result()

    def final_result(self):
        print("Primal: ")
        for dep in range(0,self.m):
            print("     ", self.primal_dep[dep], " = ", self.A[dep, self.n])

        print("Dual")
        for dep in range(0,self.n):
            print("     ", self.dual_dep[dep], " = ", self.A[self.m,dep])

    def optimal(self):
        possible_pivot_columns = np.where(self.A[self.m, 0:self.n] > 0)
        possible_pivot_columns = possible_pivot_columns[0]
        for j in possible_pivot_columns:  # Testing if the Linear Program is Unbounded
            if not self.unbounded_check(j):
                return False

        if len(possible_pivot_columns) > 1:  # If there are more than one choice, this will pass to method to decide which one
            pivot_col = self.which_row_or_col_to_use([self.primal_dep[i] for i in possible_pivot_columns], False)
        else:
            pivot_col = possible_pivot_columns[0]

        pivot_cell = [self.min(pivot_col, np.where(self.A[0:self.m, pivot_col] > 0)[0][0]), pivot_col]
        self.pivot(pivot_cell)
        return True

    def unbounded_check(self, j):  # Method That tests if a Linear Program is Unbounded, by testing a specific c_j > 0 and a column j
        if all(self.A[0:self.m, j] <= 0):
            print("********************************************************************************************************************************************************")
            print("The Linear Program is Unbounded in column: ", j, "  No Solution!")
            self.print()
            return False
        else:
            return True

    def max_basic_feasible(self):
        # loop from the bottom up, testing to see if any b_i<0.
        for i in reversed(range(0, self.m)):  # Going from bottom up for each b_i so i is maximal
            if self.A[i, self.n] < 0:  # testing to see if a pivot is needed (i.e. is b_i < 0)
                if not self.infeasible_check(i):  # if the row is infeasible, automatically ends the method
                    return False
                possible_pivot_columns = np.where(self.A[i, 0:self.n] < 0)
                if len(possible_pivot_columns[0]) > 1:  # If there are more than one choice, this will pass to method to decide which one
                    pivot_col = self.which_row_or_col_to_use([self.primal_ind[i] for i in possible_pivot_columns[0]], True)
                else:
                    pivot_col = possible_pivot_columns[0][0]
                pivot_cell = [self.min(pivot_col, i), pivot_col]
                self.pivot(pivot_cell)
                return True

    def pivot(self, pivot_cell):
        print("The Pivot Position is: ", "( ", pivot_cell[0], " , ", pivot_cell[1], " )")
        temp_primal_dep = self.primal_ind[pivot_cell[1]]  # Switching Variables of The Primal Linear Program
        self.primal_ind[pivot_cell[1]] = self.primal_dep[pivot_cell[0]]
        self.primal_dep[pivot_cell[0]] = temp_primal_dep

        temp_dual_dep = self.dual_ind[pivot_cell[0]]  # Switching Variables of the Dual Linear Program
        self.dual_ind[pivot_cell[0]] = self.dual_dep[pivot_cell[1]]
        self.dual_dep[pivot_cell[1]] = temp_dual_dep

        temp = np.copy(self.A)
        for i in range(0, self.m + 1):  # Going through each entry in the tableau
            for j in range(0, self.n + 1):
                if i == pivot_cell[0] and j != pivot_cell[1]:  # Pivot if on the same row as the pivot cell (and is not the pivot cell)
                    print("here 1")
                    print("Pivoting on: ", "( ", i, " , ", j, " )")
                    self.A[i, j] = temp[i, j] / temp[pivot_cell[0], pivot_cell[1]]
                elif j == pivot_cell[1] and i != pivot_cell[0]:  # Pivot if on the same column as the pivot cell (and is not the pivot cell)
                    print("here 2")
                    print("Pivoting on: ", "( ", i, " , ", j, " )")
                    self.A[i, j] = -1 * temp[i, j] / temp[pivot_cell[0], pivot_cell[1]]
                elif i == pivot_cell[0] and j == pivot_cell[1]:  # Pivoting on the actual pivot cell
                    print("here 3")
                    print("Pivoting on: ", "( ", i, " , ", j, " )")
                    self.A[i, j] = 1 / temp[i, j]
                else:  # All other entries
                    print("here 4")
                    print("Pivoting on: ", "( ", i, " , ", j, " )")
                    self.A[i, j] = (temp[i, j] * temp[pivot_cell[0], pivot_cell[1]] - temp[pivot_cell[0], j] * temp[i, pivot_cell[1]]) / temp[pivot_cell[0], pivot_cell[1]]
        self.print()
        print("********************************************************************************************************************************************************")

    def min(self, col, start_row):
        min_ratio = self.A[start_row, self.n] / self.A[start_row, col]
        current_row = start_row
        for i in range(start_row + 1, self.m):
            if self.A[i, col] == 0:
                continue
            if min_ratio > self.A[i, self.n] / self.A[i, col] > 0:
                min_ratio = self.A[i, self.n] / self.A[i, col]
                current_row = i
            elif self.A[i, self.n] / self.A[i, col] == min_ratio:
                current_row = self.which_row_or_col_to_use([self.primal_dep[i] for i in [current_row, i]], False)
                min_ratio = self.A[current_row, self.n] / self.A[current_row, col]
        return current_row

    def which_row_or_col_to_use(self, choices, col):  # Returns the Proper Choice According to the Order for Blands Anti Cycling Rule.
        # If choosing pivot according to columns, set col = True in the method call, else set it to false
        for bland in self.blands_rule:
            if bland in choices:
                if col:
                    return self.primal_ind.index(bland)
                else:

                    return self.primal_dep.index(bland)

    def infeasible_check(self, i):
        # This method checks if given a row of the tableau with b_i<0, it will test if the other the entries in the row are neg/pos and return false if they are indicating
        # that the tableau is infeasible
        if all(self.A[i, 0:self.n] >= 0):
            print("Tableau is Infeasible in Row: ", i, "  No Solution!")
            self.print()
            return False
        else:
            return True

