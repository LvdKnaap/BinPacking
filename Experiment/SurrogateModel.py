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
    # TODO: DOMINEERT ALLE AFWIJKINGEN
    instanceScoreTime = -solver.solveTime / customSettings.timeLimit

    # 3:
    # TODO: DIT IS ALTIJD VEEL TE DICHT BIJ 0
    instanceScoreViolations = -sum(solver.violationsPerType) / solver.numberOfConstraints

    # Normalize 2 + 3
    instanceScoreTime /= 2 * binPackingSettings.batchSize
    instanceScoreViolations /= 2 * binPackingSettings.batchSize

    # Normalize all scores over batch size
    instanceScoreSolvedInstances /= binPackingSettings.batchSize
    instanceScoreTime /= binPackingSettings.batchSize
    instanceScoreViolations /= binPackingSettings.batchSize

    # Update the score components
    self.totalScoreSolvedInstances += instanceScoreSolvedInstances
    self.totalScoreTime += instanceScoreTime
    self.totalScoreViolations += instanceScoreViolations

def updateScoreBatch(self, surrogateModelSettings, customSettings, localsAtStart):
    # calculate the maximum penalty (in case all parameters attain their most extreme value)
    maximumPenaltyRegularization = 0
    penaltyRegularizationForThisParameterConfiguration = 0
    for key in surrogateModelSettings.pbounds_bo: # loop over all variables
        # take their most extreme bound: the maximum value of the absolute values of the lower and the upper bound
        #   or: max(abs(lb), abs(ub))
        # and raise it to the exponent of the regularization factor
        maximumPenaltyRegularization += max(abs(surrogateModelSettings.pbounds_bo[key][0]), abs(surrogateModelSettings.pbounds_bo[key][1])) ** customSettings.regularizationFactorExponent


    for i in range(len(surrogateModelSettings.pbounds_bo)):
        penaltyRegularizationForThisParameterConfiguration += localsAtStart[i][1] ** customSettings.regularizationFactorExponent

    # normalize over maximum penalty:
    penaltyRegularizationForThisParameterConfiguration /= maximumPenaltyRegularization

    self.totalScoreRegularizationFactor -= customSettings.regularizationFactor * penaltyRegularizationForThisParameterConfiguration


def printInfo(self):
    print(round(self.totalScoreSolvedInstances, 2), round(self.totalScoreTime, 2), round(self.totalScoreViolations, 2),
          round(self.totalScoreRegularizationFactor, 2))

    print(round(self.totalScoreSolvedInstances + self.totalScoreTime + self.totalScoreViolations + self.totalScoreRegularizationFactor,2))


class BayesianSurrogateModel(SurrogateModel):


    def __init__(self, surrogateModelSettings, localSearchSettings, customSettings, binPackingSettings):
        self.surrogateModelSettings = surrogateModelSettings
        self.localSearchSettings = localSearchSettings
        self.customSettings = customSettings
        self.binPackingSettings = binPackingSettings


        def black_box_function(w1, w3):
            localsAtStart = list(locals().items())[:len(surrogateModelSettings.pbounds_bo)]
            localsAtStart_dict = locals()
            print(); print('attempting: ', localsAtStart)

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

                # Update the score based on the solving performance of the single instance
                updateScoreSingleInstance(self, solver, customSettings, binPackingSettings)

            # Update the score based on the solving performance of the batch
            updateScoreBatch(self, surrogateModelSettings, customSettings, localsAtStart)

            if surrogateModelSettings.printInformation_bo:
                printInfo(self)

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
            self.totalScoreSolvedInstances, self.totalScoreTime, self.totalScoreViolations, self.totalScoreRegularizationFactor = 0, 0, 0, 0;
            for i in range(binPackingSettings.batchSize):
                solver.solve(binpackingBatch.instances[i], customSettings.timeLimit)

                # Update the score based on the solving performance of the single instance
                updateScoreSingleInstance(self, solver, customSettings, binPackingSettings)

            # Update the score based on the solving performance of the batch
            updateScoreBatch(self, surrogateModelSettings, customSettings, list(params.items())[:len(surrogateModelSettings.space_ho)])

            if surrogateModelSettings.printInformation_ho:
                printInfo(self)

            return -1 * (self.totalScoreSolvedInstances + self.totalScoreTime + self.totalScoreViolations + self.totalScoreRegularizationFactor)

        # minimize the objective over the space
        best = hyperopt.fmin(
            fn=objective,
            space=surrogateModelSettings.space_ho,
            algo=hyperopt.tpe.suggest,
            max_evals=surrogateModelSettings.max_evals_ho
        )

        print(hyperopt.space_eval(surrogateModelSettings.space_ho, best))