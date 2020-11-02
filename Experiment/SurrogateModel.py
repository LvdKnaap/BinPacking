from bayes_opt import BayesianOptimization
import hyperopt as hyperopt
from Experiment.BinPacking import *
from Experiment.LocalSearch import *

class SurrogateModel:


    def __init__(self, variables, lowerbounds, upperbounds):
        self.variables = variables
        self.lowerbounds = lowerbounds
        self.upperbounds = upperbounds



def updateScoreSingleInstance(self, solver, customSettings, binPackingSettings):
    # TODO METRIC NAAR EEN LOSSE METHOD ZODAT DIE VANUIT BO EN HYPEROPT LOS AANGEROEPEN KAN WORDEN
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
        self.totalScoreSolvedInstances += customSettings.weightSolvedInstances * 1
    # TODO:  " while all non-feasible solutions have solve time equals time limit (so no deduction in term 2)"
    # dit is niet waar. Als we in een local optimum zitten die non-feasible is, kan de oplossing returnen binnen time limit.
    self.totalScoreTime += customSettings.weightTime * max(0,
                                                           customSettings.timeLimit - solver.solveTime) / binPackingSettings.batchSize
    self.totalScoreViolations += customSettings.weightViolations * solver.maximumViolationsOverViolationTypes / binPackingSettings.batchSize

def updateScoreBatch(self, surrogateModelSettings, customSettings, localsAtStart):
    # TODO: test met regularizationFactor. Minnetjes en plusjes in 1 functie moet consistent worden
    for i in range(len(surrogateModelSettings.pbounds_bo)):
        self.totalScoreRegularizationFactor += customSettings.regularizationFactor * localsAtStart[i][1] ** customSettings.regularizationFactorExponent




class BayesianSurrogateModel(SurrogateModel):


    def __init__(self, surrogateModelSettings, localSearchSettings, customSettings, binPackingSettings):
        self.surrogateModelSettings = surrogateModelSettings
        self.localSearchSettings = localSearchSettings
        self.customSettings = customSettings
        self.binPackingSettings = binPackingSettings



        def black_box_function(w1, w3):
            localsAtStart = list(locals().items())[:len(surrogateModelSettings.pbounds_bo)]
            localsAtStart_dict = locals()
            print()
            print('attempting: ', localsAtStart)

            # Create the bin packing problem instances
            binpackingBatch = BinPackingBatchCustom(binPackingSettings)

            # Create the local search solver
            solver = LocalSearch2(localSearchSettings)
            # Read all initial weights (the variable weights that are arguments to this function will be overwritten later
            solver.setInitialWeights(surrogateModelSettings)
            # Overwrite initial weights with variable weights
            solver.setVariableWeights(localsAtStart_dict)

            # Initialize score components
            self.totalScoreSolvedInstances, self.totalScoreTime, self.totalScoreViolations, self.totalScoreRegularizationFactor = 0, 0, 0, 0;
            for i in range(binPackingSettings.batchSize):
                solver.solve(binpackingBatch.instances[i], customSettings.timeLimit)
                updateScoreSingleInstance(self, solver, customSettings, binPackingSettings)
            updateScoreBatch(self, surrogateModelSettings, customSettings, localsAtStart)


            # TODO: test met regularizationFactor. Minnetjes en plusjes in 1 functie moet consistent worden
            # updateScoreBatch(self, solver, customSettings, binPackingSettings)
            # for i in range(len(surrogateModelSettings.pbounds_bo)):
            #     self.totalScoreRegularizationFactor += customSettings.regularizationFactor * localsAtStart[i][1] ** 2


            print(self.totalScoreSolvedInstances, round(self.totalScoreTime, 2), round(self.totalScoreViolations, 2),
                  round(self.totalScoreRegularizationFactor, 2))

            return self.totalScoreSolvedInstances + self.totalScoreTime + self.totalScoreViolations + self.totalScoreRegularizationFactor



        self.optimizer = BayesianOptimization(
            f=black_box_function,
            pbounds=surrogateModelSettings.pbounds_bo,
            random_state=surrogateModelSettings.randomState_bo,
        )


    def solve(self, surrogateModelSettings):
        self.optimizer.maximize(
            # alpha = self.alpha_bo
            acq=surrogateModelSettings.acq_bo,  # default acquisition function
            init_points=surrogateModelSettings.init_points_bo,
            n_iter=surrogateModelSettings.n_iter_bo,
        )















class HyperoptSurrogateModel(SurrogateModel):

    def __init__(self, surrogateModelSettings, localSearchSettings, customSettings, binPackingSettings):
        self.surrogateModelSettings = surrogateModelSettings
        self.localSearchSettings = localSearchSettings
        self.customSettings = customSettings
        self.binPackingSettings = binPackingSettings


        def objective(params):

            # TODO: CHECKEN OF DIT HET LANGZAMER MAAKT; HET LOOPEN OVER PARAMS
            if 'w1' in params:
                w1 = params['w1']
            if 'e1' in params:
                e1 = params['e1']
            if 'w2' in params:
                w2 = params['w2']
            if 'e2' in params:
                e2 = params['e2']
            if 'w3' in params:
                w3 = params['w3']
            if 'e3' in params:
                e3 = params['e3']

            print('attempting: ', [round(w1,2), round(w3,2)])

            binpackingBatch = BinPackingBatchCustom(binPackingSettings)


            # Create the local search solver
            solver = LocalSearch2(localSearchSettings)
            # Read all initial weights (the variable weights that are arguments to this function will be overwritten later
            solver.setInitialWeights(surrogateModelSettings)
            # Overwrite initial weights with variable weights
            solver.setVariableWeights(params)

            # Initialize score components
            totalScoreSolvedInstances, totalScoreTime, totalScoreViolations, totalScoreRegularizationFactor = 0, 0, 0, 0;
            # self.totalScoreSolvedInstances, self.totalScoreTime, self.totalScoreViolations, self.totalScoreRegularizationFactor = 0, 0, 0, 0;
            # for i in range(binPackingSettings.batchSize):
            #     solver.solve(binpackingBatch.instances[i], customSettings.timeLimit)
            #     updateScoreSingleInstance(self, solver, customSettings, binPackingSettings)
            # updateScoreBatch(self, surrogateModelSettings, customSettings, localsAtStart)

            for i in range(binPackingSettings.batchSize):
                solver.solve(binpackingBatch.instances[i], customSettings.timeLimit)

                if solver.curr_solutionValue == 0:
                    totalScoreSolvedInstances += customSettings.weightSolvedInstances * 1

                totalScoreTime += customSettings.weightTime * max(0,
                                                                  customSettings.timeLimit - solver.solveTime) / binPackingSettings.batchSize
                totalScoreViolations += customSettings.weightViolations * solver.maximumViolationsOverViolationTypes / binPackingSettings.batchSize

            # TODO: test met regularizationFactor. Minnetjes en plusjes in 1 functie moet consistent worden
            for wi in [w1, w3]:
                totalScoreRegularizationFactor += customSettings.regularizationFactor * wi ** 2

            print(round(totalScoreSolvedInstances + totalScoreTime + totalScoreViolations + totalScoreRegularizationFactor,2))

            return -1 * (totalScoreSolvedInstances + totalScoreTime + totalScoreViolations + totalScoreRegularizationFactor)

        # minimize the objective over the space
        best = hyperopt.fmin(
            fn=objective,
            space=surrogateModelSettings.space_ho,
            algo=hyperopt.tpe.suggest,
            max_evals=surrogateModelSettings.max_evals_ho
        )


        print(best)
        print(hyperopt.space_eval(surrogateModelSettings.space_ho, best))