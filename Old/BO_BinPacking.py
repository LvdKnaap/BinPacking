from bayes_opt import BayesianOptimization
from Old.BinPacking import *
from Old.LocalSearch import *
import random as rd

# Bounded region of parameter space
pbounds = {'useMoveAux': (0, 2), 'useSwapAux': (0, 2), 'useMergeAux': (0, 2)}


def black_box_function_optimize_noise(useMoveAux, useSwapAux, useMergeAux):
    useMove = int(useMoveAux)
    useSwap = int(useSwapAux)
    useMerge = int(useMergeAux)
    return black_box_function_discrete_noise(useMove, useSwap, useMerge)

def black_box_function_discrete_noise(useMove, useSwap, useMerge):
    assert type(useMove) == int
    assert type(useSwap) == int
    assert type(useMerge) == int

    print(useMove, useSwap, useMerge)
    binpackingInstance = BinPacking(12, 6, 100, True)
    solver = LocalSearch(useMove, useSwap, useMerge, 1000, 1, 1, 1)
    solver.solve(binpackingInstance)

    return solver.curr_solutionValue + rd.uniform(0, 1)


optimizer = BayesianOptimization(
    f = black_box_function_optimize_noise,
    pbounds=pbounds,
    random_state=1,
)

optimizer.maximize(
    alpha = 1e-2,
    # acq='ucb', # default acquisition function
    acq='ei',
    # init_points=2,
    # n_iter=1,
)

print(optimizer.max)
