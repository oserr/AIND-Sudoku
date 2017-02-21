# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: For each unit, we find pairs of squares that have the same pair of digits,
and then remove these two digits from other squres in the unit. If one or more
digits are removed from a square, then the square's new representation may yield
a constraint that can be applied to other squares, and thus constraints are
propagated.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We apply one or more constraints to each unit, which may affect squares in
the unit. Squares that are udpated may thus yield constraints that can be
applied to ther units and squares.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda][1], a pre-packaged Python distribution
that contains all of the necessary libraries and software for this project.
Please try using the environment we provided in the Anaconda lesson of the
Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization.
If you've followed our instructions for setting up our conda environment, you
should be all set.

If not, please see how to download pygame [here][2].

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running
`python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using
the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.

[1]: https://www.continuum.io/downloads
[2]: http://www.pygame.org/download.shtml

### Credit

A lot of the code in `solution.py` is in whole or partially from code used in
the presentation slides for _Solving a Sudoku with AI_.
