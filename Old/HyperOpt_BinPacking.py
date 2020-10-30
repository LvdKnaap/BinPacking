import hyperopt as hyperopt
from Old.BinPacking import *
from Old.LocalSearch import *
import random as rd


# define an objective function
# def objective(args):
#     case, val = args
#     if case == 'case 1':
#         return val
#     else:
#         return val ** 2

def objective(params):
    useMove, useSwap, useMerge = params['useMove'], params['useSwap'], params['useMerge']
    print([useMove, useSwap, useMerge])
    binpackingInstance = BinPacking(12, 6, 100, True)
    solver = LocalSearch(useMove, useSwap, useMerge, 1000, 1, 1, 1)
    solver.solve(binpackingInstance)
    print(solver.curr_solutionValue)
    print();
    return -1 * (solver.curr_solutionValue + rd.uniform(-1, 1))

# define a search space
space = {
    'useMove': hyperopt.hp.randint('useMove', 0, 3),
    'useSwap': hyperopt.hp.randint('useSwap', 0, 3),
    'useMerge': hyperopt.hp.randint('useMerge', 0, 3),
}


print(space)


# minimize the objective over the space
best = hyperopt.fmin(
    fn=objective,
    space=space,
    algo=hyperopt.tpe.suggest,
    max_evals=100
)
print(best)
print(hyperopt.space_eval(space, best))