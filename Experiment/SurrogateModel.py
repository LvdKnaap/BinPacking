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

    # 1: solved instance / batchSize
    if solver.curr_solutionValue == 0:
        instanceScoreSolvedInstances = 1
    else:
        instanceScoreSolvedInstances = 0

    # 2:
    instanceScoreTime = -solver.solveTime / customSettings.timeLimit

    # 3:
    instanceScoreTime /= 2 * binPackingSettings.batchSize

    # Normalize all scores over batch size
    instanceScoreSolvedInstances /= binPackingSettings.batchSize
    instanceScoreTime /= binPackingSettings.batchSize

    # Update the score components
    self.totalScoreSolvedInstances += instanceScoreSolvedInstances
    self.totalScoreTime += instanceScoreTime


def printInfo(self):
    print('\t\t\t\t', ['tot:', round(self.totalScoreSolvedInstances + self.totalScoreTime + self.totalScoreViolations + self.totalScoreRegularizationFactor,3),
           '    per category: ', round(self.totalScoreSolvedInstances, 3), round(self.totalScoreTime, 3), round(self.totalScoreViolations, 3),
          round(self.totalScoreRegularizationFactor, 3)])

















class BayesianSurrogateModel(SurrogateModel):


    def __init__(self, surrogateModelSettings, localSearchSettings, customSettings, binPackingSettings):
        self.surrogateModelSettings = surrogateModelSettings
        self.localSearchSettings = localSearchSettings
        self.customSettings = customSettings
        self.binPackingSettings = binPackingSettings

        def black_box_function(w1, w3):
            localsAtStart = list(locals().items())[:len(localSearchSettings.pbounds_bo)]
            localsAtStart_dict = locals()
            print('attempting: ', localsAtStart)

            # Create the bin packing problem instances
            binpackingBatch = BinPackingBatchCustom(binPackingSettings)

            # Create the local search solver
            solver = LocalSearch2(localSearchSettings)
            # Read all initial weights (the variable weights that are arguments to this function will be overwritten later
            solver.setInitialWeights(localSearchSettings)
            # Overwrite initial weights with variable weights
            solver.setVariableWeights(localsAtStart_dict)

            # Initialize score components
            self.totalScoreSolvedInstances, self.totalScoreTime, self.totalScoreViolations, self.totalScoreRegularizationFactor = 0, 0, 0, 0;
            for i in range(binPackingSettings.batchSize):
                solver.solve(binpackingBatch.instances[i], customSettings.timeLimit)

                # Update the score based on the solving performance of the single instance
                updateScoreSingleInstance(self, solver, customSettings, binPackingSettings)

            if surrogateModelSettings.printInformation_bo:
                printInfo(self)

            return self.totalScoreSolvedInstances + self.totalScoreTime + self.totalScoreViolations + self.totalScoreRegularizationFactor


        self.optimizer = BayesianOptimization(
            f=black_box_function,
            pbounds=localSearchSettings.pbounds_bo,
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
        self.count = 1


        def objective(params):
            print(["ITERATION: ", self.count]); self.count += 1
            attemptingPrint = []
            if 'w1' in params:
                w1 = params['w1']
                attemptingPrint.append(['w1', round(w1, 2)])
            if 'e1' in params:
                e1 = params['e1']
                attemptingPrint.append(['e1', round(e1, 2)])
            if 'w2' in params:
                w2 = params['w2']
                attemptingPrint.append(['w2', round(w2, 2)])
            if 'e2' in params:
                e2 = params['e2']
                attemptingPrint.append(['e2', round(e2, 2)])
            if 'w3' in params:
                w3 = params['w3']
                attemptingPrint.append(['w3', round(w3, 2)])
            if 'e3' in params:
                e3 = params['e3']
                attemptingPrint.append(['e3', round(e3, 2)])

            print('attempting: ', attemptingPrint)

            binpackingBatch = BinPackingBatchCustom(binPackingSettings)

            # Create the local search solver
            solver = LocalSearch2(localSearchSettings)

            # Read all initial weights (the variable weights that are arguments to this function will be overwritten later
            solver.setInitialWeights(localSearchSettings)
            # Overwrite initial weights with variable weights
            solver.setVariableWeights(params)

            # Initialize score components
            self.totalScoreSolvedInstances, self.totalScoreTime, self.totalScoreViolations, self.totalScoreRegularizationFactor = 0, 0, 0, 0;
            for i in range(binPackingSettings.batchSize):
                solver.solve(binpackingBatch.instances[i], customSettings.timeLimit)

                # Update the score based on the solving performance of the single instance
                updateScoreSingleInstance(self, solver, customSettings, binPackingSettings)

            # Update the score based on the solving performance of the batch
            updateScoreBatch(self, localSearchSettings, surrogateModelSettings, customSettings, list(params.items())[:len(localSearchSettings.space_ho)])

            if surrogateModelSettings.printInformation_ho:
                printInfo(self)

            return -1 * (self.totalScoreSolvedInstances + self.totalScoreTime + self.totalScoreViolations + self.totalScoreRegularizationFactor)

        # minimize the objective over the space
        best = hyperopt.fmin(
            fn=objective,
            space=localSearchSettings.space_ho,
            algo=hyperopt.tpe.suggest,
            max_evals=surrogateModelSettings.max_evals_ho,
            rstate=surrogateModelSettings.rstate_ho
        )

        print(hyperopt.space_eval(localSearchSettings.space_ho, best))