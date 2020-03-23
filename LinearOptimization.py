import numpy as np
from fractions import Fraction


def getIndexPositions(listOfElements, item):
    """ Returns the indexes of all occurrences of give element in
    the list- listOfElements """
    indexPosList = []
    for index in range(0, len(listOfElements)):
        if listOfElements[index] == item:
            indexPosList.insert(len(indexPosList), index)
    return indexPosList


def getIndexPositionsThatStartWith(listOfElements, item):
    """ Returns the indexes of all occurrences of give element in
    the list- listOfElements """
    indexPosList = []
    for index in range(0, len(listOfElements)):
        if listOfElements[index].startswith(item):
            indexPosList.insert(len(indexPosList), index)
    return indexPosList


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
            self.primal_ind = self.__variable_creator("x", self.n) + ["-1"]
            self.primal_dep = self.__variable_creator("t", self.m) + ["f"]
        elif not primal_independent:  # Only Dependent Vars are specified in the class call
            self.primal_ind = self.__variable_creator("x", self.n) + ["-1"]
            self.primal_dep = primal_dependent + ["f"]
        elif not primal_independent:  # Only Independent Vars are specified in the class call
            self.primal_ind = primal_independent + ["-1"]
            self.primal_dep = self.__variable_creator("t", self.m) + ["f"]

        self.blands_rule = self.primal_ind + self.primal_dep  # Initializes Variable Order for Blands Anti Cycling Rule

        self.dual_ind = self.__dual_variable_creator("y", self.m, True) + ["-1"]
        self.dual_dep = self.__dual_variable_creator("s", self.n, False) + ["g"]

        self.primal_recorded_equations = []
        self.dual_recorded_equations = []

    def __dual_variable_creator(self, var, iterable, dual_primal):  # Based on the constraints of the primal LP, it creates the variables and constrains of the Dual LP
        variables = [var] * iterable
        for j in range(0, iterable):
            if not dual_primal:
                if self.primal_ind[j].startswith("*"):  # Testing for Equality in the Constraints
                    variables[j] = '0'
                else:
                    variables[j] = var + str(j + 1)
            else:
                if self.primal_dep[j] == '0':  # Testing for Equality in the Constraints
                    variables[j] = '*' + var + str(j + 1)
                else:
                    variables[j] = var + str(j + 1)
        return variables

    def __variable_creator(self, var, iterable):
        variables = [var] * iterable
        for j in range(0, iterable):
            variables[j] = var + str(j + 1)
        return variables

    def print(self):
        # problem_complete = [""]
        # [problem_complete.insert(len(problem_complete),i) for i in self.primal_ind]
        # for i in range(0,self.m):
        #     problem_complete.insert(len(problem_complete),self.dual_ind[i])
        #     [problem_complete.insert(len(problem_complete), elem) for elem in self.A[i,:]]
        #     problem_complete.insert(len(problem_complete),self.primal_dep[i])
        # [problem_complete.insert(len(problem_complete), j) for j in self.dual_dep]
        #
        # for i in range(0,self.m):
        #     for j in range(0,self.n):
        #         print(problem_complete[i+j])
        #         print()
        # print(problem_complete)
        print("A = ", self.A)
        print("Primal Independent Variables: ", self.primal_ind)
        print("Primal Dependent Variables: ", self.primal_dep)
        print("Dual Independent Variables: ", self.dual_ind)
        print("Dual Dependent Variables: ", self.dual_dep)

    def simplex_algorithm(self):
        self.print()
        print("************************************************************************************************************************")
        print("************************************************************************************************************************")
        primal_equality_constraints = getIndexPositions(self.primal_dep, '0')
        primal_unconstrained_variables = getIndexPositionsThatStartWith(self.primal_ind, "*")

        while len(primal_equality_constraints) > 0 and len(primal_unconstrained_variables) > 0:
            if self.A[primal_equality_constraints[0], primal_unconstrained_variables[0]] == 0:  # Testing if it tries to pivot on a zero.  If so it passes to the method that is equipped to deal with it
                self.removing_primal_unconstrained_variables(primal_unconstrained_variables)
                primal_equality_constraints = getIndexPositions(self.primal_dep, '0')
                primal_unconstrained_variables = getIndexPositionsThatStartWith(self.primal_ind, "*")
                continue
            self.__pivot([primal_equality_constraints[0], primal_unconstrained_variables[0]])

            # Recording Rows and Columns of the Tableau
            self.primal_recorded_equations.insert(len(self.primal_recorded_equations), [self.A[primal_equality_constraints[0], :], self.primal_ind[:], self.primal_dep[primal_equality_constraints[0]]])
            self.dual_recorded_equations.insert(len(self.dual_recorded_equations), [self.A[:, primal_unconstrained_variables[0]], self.dual_ind[:], self.dual_dep[primal_unconstrained_variables[0]]])

            # Deleting the Corresponding Variables
            del self.primal_ind[primal_unconstrained_variables[0]]
            del self.primal_dep[primal_equality_constraints[0]]
            del self.dual_ind[primal_equality_constraints[0]]
            del self.dual_dep[primal_unconstrained_variables[0]]

            # Deleting Rows and Columns of the Tableau
            self.A = np.delete(self.A, primal_equality_constraints[0], axis=0)
            self.m = self.m - 1
            self.A = np.delete(self.A, primal_unconstrained_variables[0], axis=1)
            self.n = self.n - 1

            # Resetting the Variables
            primal_equality_constraints = getIndexPositions(self.primal_dep, '0')
            primal_unconstrained_variables = getIndexPositionsThatStartWith(self.primal_ind, "*")
            self.print()

        if len(primal_unconstrained_variables) > 0:
            self.removing_primal_unconstrained_variables(primal_unconstrained_variables)

        if len(primal_equality_constraints) > 0:
            self.removing_equality_constraints(primal_equality_constraints)

        while any(self.A[0:self.m, self.n] < 0):  # Testing if the Tableau is Maximum Basic Feasible
            if not self.__max_basic_feasible():
                return

        while any(self.A[self.m, 0:self.n] > 0):  # Testing if the Tableau is Optimal
            if not self.__optimal():
                return

    def removing_equality_constraints(self,pec):
        primal_equality_constraints = pec
        while len(primal_equality_constraints) > 0:
            try:
                pivot_row = int(np.where(self.A[primal_equality_constraints[0], 0:self.n] != 0)[0][0])
            except IndexError as error:
                print(error)
                print('The LP as entered cannot be converted into canonical form, please check the tableau for incorrect entries.  Look for a row of zeros in row: ', primal_equality_constraints[0])

            self.__pivot([primal_equality_constraints[0], pivot_row])

            # Recording Rows and Columns of the Tableau
            self.dual_recorded_equations.insert(len(self.dual_recorded_equations), [self.A[:, pivot_row], self.dual_ind[:], self.dual_dep[pivot_row]])

            # Deleting the Corresponding Variables
            del self.primal_ind[pivot_row]
            del self.dual_dep[pivot_row]

            # Deleting Rows and Columns of the Tableau
            self.A = np.delete(self.A, pivot_row, axis=1)
            self.n = self.n - 1

            # Resetting the Variables
            primal_equality_constraints = getIndexPositions(self.primal_dep, '0')
            self.print()
            print("************************************************************************************************************************")

    def removing_primal_unconstrained_variables(self, puc):
        primal_unconstrained_variables = puc
        while len(primal_unconstrained_variables) > 0:
            try:
                pivot_row = int(np.where(self.A[primal_unconstrained_variables[0], 0:self.n] != 0)[0][0])
            except IndexError as error:
                print(error)
                print('The LP as entered cannot be converted into canonical form, please check the tableau for incorrect entries.  Look for a column of zeros in row: ', primal_unconstrained_variables[0])

            pivot_row = int(pivot_row)

            # Pivoting
            self.__pivot([pivot_row, primal_unconstrained_variables[0]])

            # Recording Rows and Columns of the Tableau
            self.primal_recorded_equations.insert(len(self.primal_recorded_equations), [self.A[pivot_row, :], self.primal_ind[:], self.primal_dep[pivot_row]])

            # Deleting the Corresponding Variables
            del self.primal_dep[pivot_row]
            del self.dual_ind[pivot_row]

            # Deleting Rows and Columns of the Tableau
            self.A = np.delete(self.A, pivot_row, axis=0)
            self.m = self.m - 1

            # Reset Variables
            primal_unconstrained_variables = getIndexPositionsThatStartWith(self.primal_ind, "*")
            self.print()
            print("************************************************************************************************************************")

    def __final_result(self):
        print("Primal: ")
        for dep in range(0, self.m):
            print("     ", self.primal_dep[dep], " = ", self.A[dep, self.n])

        print("Dual")
        for dep in range(0, self.n):
            print("     ", self.dual_dep[dep], " = ", self.A[self.m, dep])

    def __optimal(self):
        possible_pivot_columns = np.where(self.A[self.m, 0:self.n] > 0)
        possible_pivot_columns = possible_pivot_columns[0]
        for j in possible_pivot_columns:  # Testing if the Linear Program is Unbounded
            if not self.__unbounded_check(j):
                return False

        if len(possible_pivot_columns) > 1:  # If there are more than one choice, this will pass to method to decide which one
            pivot_col = self.__which_row_or_col_to_use([self.primal_dep[i] for i in possible_pivot_columns], False)
        else:
            pivot_col = possible_pivot_columns[0]

        pivot_cell = [self.__min(pivot_col, np.where(self.A[0:self.m, pivot_col] > 0)[0][0]), pivot_col]
        self.__pivot(pivot_cell)
        return True

    def __unbounded_check(self, j):  # Method That tests if a Linear Program is Unbounded, by testing a specific c_j > 0 and a column j
        if all(self.A[0:self.m, j] <= 0):
            print("The Linear Program is Unbounded in column: ", j, "  No Solution!")
            self.print()
            return False
        else:
            return True

    def __max_basic_feasible(self):
        # loop from the bottom up, testing to see if any b_i<0.
        for i in reversed(range(0, self.m)):  # Going from bottom up for each b_i so i is maximal
            if self.A[i, self.n] < 0:  # testing to see if a pivot is needed (i.e. is b_i < 0)
                if not self.__infeasible_check(i):  # if the row is infeasible, automatically ends the method
                    return False
                possible_pivot_columns = np.where(self.A[i, 0:self.n] < 0)
                if len(possible_pivot_columns[0]) > 1:  # If there are more than one choice, this will pass to method to decide which one
                    pivot_col = self.__which_row_or_col_to_use([self.primal_ind[i] for i in possible_pivot_columns[0]], True)
                else:
                    pivot_col = possible_pivot_columns[0][0]
                pivot_cell = [self.__min(pivot_col, i), pivot_col]
                self.__pivot(pivot_cell)
                return True

    def __pivot(self, pivot_cell):
        print("The Pivot Position is: ", "( ", pivot_cell[0], " , ", pivot_cell[1], " ).  This gives: ")
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
                    self.A[i, j] = temp[i, j] / temp[pivot_cell[0], pivot_cell[1]]
                elif j == pivot_cell[1] and i != pivot_cell[0]:  # Pivot if on the same column as the pivot cell (and is not the pivot cell)
                    self.A[i, j] = -1 * temp[i, j] / temp[pivot_cell[0], pivot_cell[1]]
                elif i == pivot_cell[0] and j == pivot_cell[1]:  # Pivoting on the actual pivot cell
                    self.A[i, j] = 1 / temp[i, j]
                else:  # All other entries
                    self.A[i, j] = (temp[i, j] * temp[pivot_cell[0], pivot_cell[1]] - temp[pivot_cell[0], j] * temp[i, pivot_cell[1]]) / temp[pivot_cell[0], pivot_cell[1]]

    def __min(self, col, start_row):
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

    def __which_row_or_col_to_use(self, choices, col):  # Returns the Proper Choice According to the Order for Blands Anti Cycling Rule.
        # If choosing pivot according to columns, set col = True in the method call, else set it to false
        for bland in self.blands_rule:
            if bland in choices:
                if col:
                    return self.primal_ind.index(bland)
                else:

                    return self.primal_dep.index(bland)

    def __infeasible_check(self, i):
        # This method checks if given a row of the tableau with b_i<0, it will test if the other the entries in the row are neg/pos and return false if they are indicating
        # that the tableau is infeasible
        if all(self.A[i, 0:self.n] >= 0):
            print("Tableau is Infeasible in Row: ", i, "  No Solution!")
            self.print()
            return False
        else:
            return True
