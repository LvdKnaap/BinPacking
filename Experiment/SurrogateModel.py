from bayes_opt import BayesianOptimization
from Experiment.BinPackingBatch import *
from Old.LocalSearch2 import * # todo moet weg


class SurrogateModel:


    def __init__(self, variables, lowerbounds, upperbounds):
        self.variables = variables
        self.lowerbounds = lowerbounds
        self.upperbounds = upperbounds



class BayesianSurrogateModel(SurrogateModel):


    def __init__(self, surrogateModelSettings, localSearchSettings, customSettings, binPackingSettings):
        self.surrogateModelSettings = surrogateModelSettings
        self.localSearchSettings = localSearchSettings
        self.customSettings = customSettings
        self.binPackingSettings = binPackingSettings

        def black_box_function(w1, w3):
            localsAtStart = list(locals().items())[:len(surrogateModelSettings.pbounds)]
            print()
            print('attempting: ', localsAtStart)

            binpackingBatch = BinPackingBatchCustom(binPackingSettings.batchSizeType1, binPackingSettings.batchSizeType2, binPackingSettings.batchSizeType3, binPackingSettings.batchSizeType4,
                                                    binPackingSettings.batchSizeType5)
            totalScoreSolvedInstances, totalScoreTime, totalScoreViolations, totalScoreRegularizationFactor = 0, 0, 0, 0;

            # solver = LocalSearch2(1, 1, 1, 2 ** w1, e1, 2 ** w2, e2, 2 ** w3, e3)
            solver = LocalSearch2(1, 1, 1, 2 ** w1, 1, 1, 1, 2 ** w3, 1, localSearchSettings.simulatedAnnealing, 10, 10, 0.99)
            for i in range(binPackingSettings.batchSize):
                solver.solve(binpackingBatch.instances[i], customSettings.timeLimit)

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
                    totalScoreSolvedInstances += customSettings.weightSolvedInstances * 1
                # TODO:  " while all non-feasible solutions have solve time equals time limit (so no deduction in term 2)"
                # dit is niet waar. Als we in een local optimum zitten die non-feasible is, kan de oplossing returnen binnen time limit.
                totalScoreTime += customSettings.weightTime * max(0, customSettings.timeLimit - solver.solveTime) / binPackingSettings.batchSize
                totalScoreViolations += customSettings.weightViolations * solver.maximumViolationsOverViolationTypes / binPackingSettings.batchSize

            # TODO: test met regularizationFactor. Minnetjes en plusjes in 1 functie moet consistent worden
            for i in range(len(surrogateModelSettings.pbounds)):
                totalScoreRegularizationFactor += customSettings.regularizationFactor * localsAtStart[i][1] ** 2

            print(totalScoreSolvedInstances, round(totalScoreTime, 2), round(totalScoreViolations, 2),
                  round(totalScoreRegularizationFactor, 2))
            return totalScoreSolvedInstances + totalScoreTime + totalScoreViolations + totalScoreRegularizationFactor


        self.optimizer = BayesianOptimization(
            f=black_box_function,
            pbounds=surrogateModelSettings.pbounds,
            random_state=surrogateModelSettings.randomState,
        )

    def solve(self, surrogateModelSettings):
        self.optimizer.maximize(
            # alpha = self.alpha
            acq=surrogateModelSettings.acq,  # default acquisition function
            # acq='ei',
            init_points=surrogateModelSettings.init_points,
            n_iter=surrogateModelSettings.n_iter,
        )













class HyperoptSurrogateModel(SurrogateModel):

    def __init__(self, surrogateModelSettings, localSearchSettings, customSettings, binPackingSettings):
        self.surrogateModelSettings = surrogateModelSettings
        self.localSearchSettings = localSearchSettings
        self.customSettings = customSettings
        self.binPackingSettings = binPackingSettings