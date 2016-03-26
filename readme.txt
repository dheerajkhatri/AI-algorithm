Exercise 1. Consider the 15-puzzle problem with Manhattan distance heuristic function. The goal state
is given below:
1 2 3
4 5 6 7
8 9 10 11
12 13 14 15
Apply A* and IDA* algorithms to the given problem with 20 randomly generated initial states and
comment and compare their results. Tabulate the results as shown below and plot the same.
Number Initial State Length of
Optimal Solution
Number of
nodes
generated
A* IDA* A* IDA*
1.
… … … … … …
20.



Exercise 2. Consider the 15-puzzle problem with Manhattan distance heuristic function. The goal state is
given below:
1 2 3
4 5 6 7
8 9 10 11
12 13 14 15
Apply IDA* and RBFS algorithms to the given problem with 20 randomly generated initial states and
comment and compare their results. Tabulate the results as shown below.
Bonus points: apply the same algorithms with weighted heuristic function such that the cost function is
non-monotonic and see how bad the solutions are.


Exercise 3. Generate at least 20 instances of 8-queens and solve them using random restart hill-climbing
and simulated annealing. Measure the percentage of solved problems and plot. Comment on your
results.


Exercise 4. Solve 8-queens problem using genetic algorithm with single point cross over, roulette wheel
selection and very small mutation probability. Comment and compare your results for various instances
of initial population.


Exercise 5. Construct a game playing agent using alpha-beta pruning for tic-tac-toe game. Assume your
own move generators and evaluation function. What is the effective branching factor? Can you improve
this by improving the move ordering? Comment on your results. 