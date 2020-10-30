from bayes_opt import BayesianOptimization
from BinPacking2 import *
from LocalSearch2 import *
import random as rd
import numpy as np



class SurrogateModel:


    def __init__(self, variables, lowerbounds, upperbounds):
        self.variables = variables
        self.lowerbounds = lowerbounds
        self.upperbounds = upperbounds



class BayesianSurrogateModel(SurrogateModel):


    def __init__(self, bounds, settings):
        self.pbounds = bounds
        self.settings = settings

        def black_box_function(w1, w3):
            localsAtStart = list(locals().items())[:len(self.pbounds)]
            print()
            print('attempting: ', localsAtStart)

            binpackingBatch = BinPackingBatchCustom(settings.batchSizeType1, settings.batchSizeType2, settings.batchSizeType3, settings.batchSizeType4,
                                                    settings.batchSizeType5)
            totalScoreSolvedInstances, totalScoreTime, totalScoreViolations, totalScoreRegularizationFactor = 0, 0, 0, 0;

            # solver = LocalSearch2(1, 1, 1, 2 ** w1, e1, 2 ** w2, e2, 2 ** w3, e3)
            solver = LocalSearch2(1, 1, 1, 2 ** w1, 1, 1, 1, 2 ** w3, 1, settings.simulatedAnnealing, 10, 10, 0.99)
            for i in range(settings.batchSize):
                solver.solve(binpackingBatch.instances[i], settings.timeLimit)

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
                    totalScoreSolvedInstances += settings.weightSolvedInstances * 1
                # TODO:  " while all non-feasible solutions have solve time equals time limit (so no deduction in term 2)"
                # dit is niet waar. Als we in een local optimum zitten die non-feasible is, kan de oplossing returnen binnen time limit.
                totalScoreTime += settings.weightTime * max(0, settings.timeLimit - solver.solveTime) / settings.batchSize
                totalScoreViolations += settings.weightViolations * solver.maximumViolationsOverViolationTypes / settings.batchSize

            # TODO: test met regularizationFactor. Minnetjes en plusjes in 1 functie moet consistent worden
            for i in range(len(self.pbounds)):
                totalScoreRegularizationFactor += settings.regularizationFactor * localsAtStart[i][1] ** 2

            print(totalScoreSolvedInstances, round(totalScoreTime, 2), round(totalScoreViolations, 2),
                  round(totalScoreRegularizationFactor, 2))
            return totalScoreSolvedInstances + totalScoreTime + totalScoreViolations + totalScoreRegularizationFactor


        self.optimizer = BayesianOptimization(
            f=black_box_function,
            pbounds=self.pbounds,
            random_state=settings.randomState,
        )

    def solve(self, settings):
        self.optimizer.maximize(
            # alpha = self.alpha
            acq=settings.acq,  # default acquisition function
            # acq='ei',
            init_points=settings.n_iter,
            n_iter=settings.n_iter,
        )

    def printTest(self):
        print('mag weg')















class HyperoptSurrogateModel(SurrogateModel):

    def __init__(self, variables, lowerbounds, upperbounds):
        self.variables = variables
        self.lowerbounds = lowerbounds
        self.upperbounds = upperbounds

    def printTest(self):
        print('mag weg')


