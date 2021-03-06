from bayes_opt import BayesianOptimization
from Old.BinPacking2 import *
from Old.LocalSearch2 import *

##### HYPERPARAMETERS <3
timeLimit = 0.5 # in seconds
weightSolvedInstances = 1
weightTime = 0.1
weightViolations = -0.1
regularizationFactor = -0.002

###########################
simulatedAnnealing = True
batchSizeType1 = 2
batchSizeType2 = 2
batchSizeType3 = 2
batchSizeType4 = 0
batchSizeType5 = 2
batchSize = batchSizeType1 + batchSizeType2 + batchSizeType3 + batchSizeType4 + batchSizeType5
##########################


# Bounded region of parameter space
# pbounds = {'w1': (-5, 5), 'e1': (-2, 4), 'w2': (-5, 5), 'e2': (-3, 2), 'w3': (-5, 5), 'e3': (-1, 4)}
pbounds = {'w1': (-10, 10), 'w3': (-1, 3)}

# def black_box_function(w1, e1, w2, e2, w3, e3):
def black_box_function(w1, w3):
    localsAtStart = locals()
    print()
    print('attempting: ', localsAtStart)

    binpackingBatch = BinPackingBatchCustom(batchSizeType1, batchSizeType2, batchSizeType3, batchSizeType4, batchSizeType5)
    totalScoreSolvedInstances, totalScoreTime, totalScoreViolations, totalScoreRegularizationFactor = 0, 0, 0, 0;

    # solver = LocalSearch2(1, 1, 1, 2 ** w1, e1, 2 ** w2, e2, 2 ** w3, e3)
    solver = LocalSearch2(1, 1, 1, 2 ** w1, 1, 1, 1, 2 ** w3, 1, simulatedAnnealing, 10, 10, 0.99)
    for i in range(batchSize):
        solver.solve(binpackingBatch.instances[i], timeLimit)

        # THE CURRENT METRIC IS:
        #     1) the number of solved instances +
        #     2) avg seconds below time limit per instance * weight -

        # TODO: is een test. is dit logischer dan som over violations en is het correct geimplementeerd?
        #     3) maximum (over all violation types) violations of a type  * weight
        # todo: RETURNT IN IEDER GEVAL TE HOGE PENALTIES!!!!
        # first term most important, 2nd and 3rd to get some differences
        # important to note: all feasible solutions have violations = 0 (so no deduction in term 3)
        #     while all non-feasible solutions have solve time equals time limit (so no deduction in term 2)

        if solver.curr_solutionValue == 0:
            totalScoreSolvedInstances += weightSolvedInstances * 1
        # TODO:  " while all non-feasible solutions have solve time equals time limit (so no deduction in term 2)"
            # dit is niet waar. Als we in een local optimum zitten die non-feasible is, kan de oplossing returnen binnen time limit.
        totalScoreTime += weightTime * max(0, timeLimit - solver.solveTime) / batchSize
        totalScoreViolations += weightViolations * solver.maximumViolationsOverViolationTypes / batchSize


    # TODO: test met regularizationFactor. Minnetjes en plusjes in 1 functie moet consistent worden
    for keyOfFunctionArgument in localsAtStart:
        totalScoreRegularizationFactor += regularizationFactor * localsAtStart.get(keyOfFunctionArgument) ** 2

    print(totalScoreSolvedInstances, round(totalScoreTime,2), round(totalScoreViolations,2), round(totalScoreRegularizationFactor, 2))
    return totalScoreSolvedInstances + totalScoreTime + totalScoreViolations + totalScoreRegularizationFactor


optimizer = BayesianOptimization(
    f = black_box_function,
    pbounds=pbounds,
    random_state=13,
)

optimizer.maximize(
    # alpha = 1e-2,
    acq='ucb', # default acquisition function
    # acq='ei',
    init_points=3,
    n_iter=10,
)

print(optimizer.max)
