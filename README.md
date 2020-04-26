# Simplex Algorithm Solver for SFU MATH 308: Linear Optimization

## Abstract
This solver was developed due to an apparent absence of online solvers that used Tucker Tableau's while performing the simplex algorithm.  To be specific, this solver targets the output required for MATH 308, Linear Optimization at Simon Fraser University in Burnaby, BC.  It should also be noted that this solver was absolutely not written with efficiency in mind and was purely created to follow the neccessary steps, and to produce the output required for the class.  Examples of the variation of the Simplex Algorithm used can be found in the text Linear Programming and Its Applications by James K. Strayer. 

## How to use it:
Inputting a tucker tableau into the solver is fairly straight forward.  Four examples are given below.

### Example 1
The following example is taken from tableau given on page 51 of text.  To begin, store the elements as a numpy array, and create an Optimization object.  To execute the simplex algorithm call the simplex_algorithm() method. 
```python
import LinearOptimization as LO
import numpy as np

A = np.array([[-1, -2, -3], [1, 1, 3], [1, 1, 2], [-2, 4, 0]])

example = LO.Optimizer(A)

example.simplex_algorithm()
```

### Example 2
The solver also can except non-canonical Tableau's as well.  Consider the example from page 81 of the text.
```python
import LinearOptimization as LO
import numpy as np

A = np.array([[1, 1, 1, 6], [1, 1, 0, 1], [1, 2, 1, 0]])

example = LO.Optimizer(A, primal_independent=["*x", "y", "z"], primal_dependent=["0", "t"])

example.simplex_algorithm()
```
Note two things in this example.  
1. Notice the asterisk in front of the y in the primal_dependent variables.  This denotes y as a variable with no non-negativity constrain.  
2. Notice the zero in the first element of the primal_independent variables.  This denotes an equality constrain in the constraint set.
3. THe user can specify the variable names for the primal linear program (NOTE: the user cannot specify the variables of the dual linear program, they are generated automatically by the program)

### Example 3
Consider the example from page 36 of the text.  In this linear program we wish to minimize the objective function.  To perform this in the solver, the user can either transpose the tableau so as to maximize the objective function, or simply enter linear program as is and the solver will execute the dual simplex algorithm which will of course still give the minimized objective function. 
```python
import LinearOptimization as LO
import numpy as np

A = np.array([[1, 2, 20], [2, 2, 30], [2, 1, 25], [200, 150, 0]])

example = LO.Optimizer(A)

example.simplex_algorithm()
```

### Example 4
This example is taken from question 5 (b) on page 110 of the text.  
```python
import LinearOptimization as LO
import numpy as np

A = np.array([[-2, 1, -2], [1, -1, -1], [1, 1, 0]])

example = LO.Optimizer(A, primal_independent=["*x", "y", "z"], primal_dependent=["0", "t"])

example.simplex_algorithm()
```

And the programs final output:
```
The Linear Program is Unbounded in column:  0   No Solution!
A =  [[-2.  4.]
 [ 3. -7.]]
Primal Independent Variables:  ['t', 'z', '-1']
Primal Dependent Variables:  ['y', 'f']
Dual Independent Variables:  ['s2', '-1']
Dual Dependent Variables:  ['y2', 'g']
Primal Stored Equations:  [[array([-0.5, -0.5,  1. ]), ['0', 'y', 'z', '-1'], '*x']]
Dual Stored Equations:  [[array([-0.5,  0.5,  0.5]), ['0', 'y2', '-1'], '*y1']]
```

Note in this example the program stops executing when it is noticed that the primal linear program is unbounded in column 0.  With respect to the primal linear program, the pogram will always stop executing when the linear program is know to be either infeasible or unbounded.  HOWEVER, it will not detect of the dual is infeasible or unbounded. Interpreting this is left to the user as it is usually only a matter of examining the final tableau. 

### A Few Things to Note:
1. The solver only executes the primal simplex algorithm (i.e. a maximization linear program).  However it does keep track of the dual variables and as such can be used to solve the dual linear program as well
2. As seen in example 2, the solver excepts non-canonical linear programs.  In the case where equations need to be recorded, the recorded equations will be produced after each pivot.  Consider the final output from example 2 shown below:
    ```
    A =  [[-0. -1.  5.]
     [-1. -1. -7.]]
    Primal Independent Variables:  ['x', 't', '-1']
    Primal Dependent Variables:  ['z', 'f']
    Dual Independent Variables:  ['s3', '-1']
    Dual Dependent Variables:  ['s1', 'y2', 'g']
    Primal Stored Equations:  [[array([1., 1., 1., 6.]), ['x', '0', 'z', '-1'], '*y']]
    Dual Stored Equations:  [[array([ 1., -1., -2.]), ['0', 'y2', '-1'], '*y1']]
    ```
    In the output here, the program will output the corresponding variables.  It is left to the user to associate where each variable should be place in relation to the tableau.  WIth respect to the stored equations, it can be seen that in the primal stored equation the outputed equation is for example "1*x + 1*0 + 1*x + 1*z +6*-1 = -y".
    It is then left to the user to derive the final solution by hand.
3. The solver is only designed to apply the necessary pivots up to the final optimal tableau, or earlier if program is unbounded or infeasible.  It is generally left to the user to interpret the final solution from the output.
