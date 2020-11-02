import numpy as np
import random as rd
import time
import math

# Local search 2 tov 1
#     stopping criteria voor tijd
#     items kunnen ook NIET assigned zijn
#         initial solution is alle items aan 0 bins assigned
#         'move' kan ook een item assignen naar géén bin

# TODO: HYPERPARAMETER OM NEIGHBOORHOOD RULES IN ISOLATION TE RUNNEN
# TODO: localsearch moet extended worden door simulated annealing of variable neighboorhood
    # of andere manier hiervoor


class LocalSearch2:
    # Local search rules:
    # // weight parameters
    w1 = 0
    e1 = 0
    w2 = 0
    e2 = 0
    w3 = 0
    e3 = 0
    localSearchSettings = ""

    localSearchtype = ""

    # stopping criteria:
    budget_evaluations = 0
    timeLimit = 0
    startTime = 0
    solveTime = 0
    maximumViolationsOverViolationTypes = 0

    curr_solutionValue = False;
    curr_solution = 0;

    def __init__(self,localSearchSettings):
        self.localSearchSettings = localSearchSettings

        if localSearchSettings.simulatedAnnealing:
            self.localSearchtype = 'SA'
        elif localSearchSettings.variableNeighborhoodSearch:
            self.localSearchtype = 'VNS'
        else:
            self.localSearchtype = 'HC' # hill climbing



    def solve(self, binPackingInstance, timeLimit):
        self.curr_solution = self.createInitialSolution(binPackingInstance)
        [self.curr_solutionValue, self.maximumViolationsOverViolationTypes] = binPackingInstance.evaluate(self.curr_solution, self.w1, self.e1, self.w2, self.e2, self.w3, self.e3)
        self.timeLimit = timeLimit
        self.startTime = time.time()

        improved = True;
        while improved and not self.shouldWeTerminate():
            improved = self.performOneIteration(binPackingInstance)
        # register the end time
        self.solveTime = round(time.time() - self.startTime, 3)


    def performOneIteration(self, binPackingInstance):
        return self.merge(binPackingInstance, self.curr_solution) # eerst merge, dan swap, dan move
        return False




    def merge(self, binPackingInstance, input_solution):
        if self.shouldWeTerminate():
            return False

        if self.localSearchSettings.useMerge == 1:
            binOrder1 = list(range(binPackingInstance.numBins))
            rd.shuffle(binOrder1)
            binOrder2 = list(range(binPackingInstance.numBins))
            rd.shuffle(binOrder2)

            for bin1 in binOrder1:
                for bin2 in binOrder2:
                    # // create new solution and put all items from bin2 in bin1
                    new_solution = np.copy(input_solution)
                    for i in range(binPackingInstance.numItems):
                        if new_solution[i][bin2]:
                            new_solution[i][bin2] = False
                            new_solution[i][bin1] = True

                    if self.swap(binPackingInstance, new_solution):
                        return True

        else:
            if self.swap(binPackingInstance, input_solution):
                return True
        return False


    def swap(self, binPackingInstance, input_solution):
        if self.shouldWeTerminate():
            return False

        if self.localSearchSettings.useSwap == 1:
            itemOrder1 = list(range(binPackingInstance.numItems))
            rd.shuffle(itemOrder1)
            itemOrder2 = list(range(binPackingInstance.numItems))
            rd.shuffle(itemOrder2)
            for item1 in itemOrder1:
                for item2 in itemOrder2:
                    # create new solution
                    new_solution = np.copy(input_solution)

                    oldBinItem1 = -1
                    oldBinItem2 = -1
                    for bin in range(binPackingInstance.numBins):
                        if new_solution[item1][bin]:
                            oldBinItem1 = bin
                        if new_solution[item2][bin]:
                            oldBinItem2 = bin
                    # perform swap
                    new_solution[item1][oldBinItem1] = False
                    new_solution[item2][oldBinItem2] = False
                    new_solution[item1][oldBinItem2] = True
                    new_solution[item2][oldBinItem1] = True

                    if self.move(binPackingInstance, new_solution):
                        return True

        else:
            if self.move(binPackingInstance, input_solution):
                return True

        return False




    def move(self, binPackingInstance, input_solution):
        self.localSearchSettings.evaluations += 1

        if self.shouldWeTerminate():
            return False

        if self.localSearchSettings.useMove == 1:
            itemOrder = list(range(binPackingInstance.numItems))
            rd.shuffle(itemOrder)
            # binOrder = list(range(binPackingInstance.numBins))
            binOrder = list(range(binPackingInstance.numBins+1)) # stap 1 om te testen of we aan géén bin kunnen toewijzen
            rd.shuffle(binOrder)
            for i in itemOrder:
                for j in binOrder:
                    new_solution = np.copy(input_solution)
                    # remove assignment to order bins
                    for binIndex in range(binPackingInstance.numBins):
                        new_solution[i][binIndex] = False
                    # perform the move
                    if j < binPackingInstance.numBins: # stap 2 om te testen of we aan géén bin kunnen toewijzen
                        new_solution[i][j] = True


                    # accept or not?
                    if self.acceptOrNot(binPackingInstance, new_solution):
                        return True
        else:
            # accept or not?
            if self.acceptOrNot(binPackingInstance, input_solution):
                return True
        return False

    def acceptOrNot(self, binPackingInstance, new_solution):

        # decrease temperature periodically
        if self.localSearchSettings.evaluations % self.localSearchSettings.iterationsPerTemperatureReduction == 0:
            self.localSearchSettings.temperature = self.localSearchSettings.temperatureReductionFactor * self.localSearchSettings.temperature;

        # always accept improvements:
        if binPackingInstance.evaluate(new_solution, self.w1, self.e1, self.w2, self.e2, self.w3, self.e3)[0] > self.curr_solutionValue:  # > because maximizatione
            [self.curr_solutionValue, self.maximumViolationsOverViolationTypes] = binPackingInstance.evaluate(
                new_solution, self.w1, self.e1, self.w2, self.e2, self.w3, self.e3)
            self.curr_solution = new_solution
            return True

        elif self.localSearchSettings.simulatedAnnealing:
            acceptProbability = math.exp((binPackingInstance.evaluate(new_solution, self.w1, self.e1, self.w2, self.e2, self.w3, self.e3)[0] - self.curr_solutionValue)/self.localSearchSettings.temperature)
            if rd.uniform(0, 1) < acceptProbability: # accept
                [self.curr_solutionValue, self.maximumViolationsOverViolationTypes] = binPackingInstance.evaluate(
                    new_solution, self.w1, self.e1, self.w2, self.e2, self.w3, self.e3)
                self.curr_solution = new_solution
                return True
        return False


    def createInitialSolution(self, binPackingInstance):
        # Each item in bin 1
        initialSolution = np.zeros((binPackingInstance.numItems, binPackingInstance.numBins))
        return initialSolution


    def shouldWeTerminate(self):
        # Check if we already found the optimal (ie a feasible) solution. If so, we can terminate
        if self.curr_solutionValue == 0:
            return True

        # Check if the time limit has been exceeded. If so, we can terminate
        if time.time() - self.startTime > self.timeLimit:
            return True

        # base
        return False

    # Set all weights to specified in settings. They will be overwritten by setVariableWeights
    def setInitialWeights(self, surrogateModelSettings):
        self.w1 = surrogateModelSettings.fixedParameters['w1']
        self.e1 = surrogateModelSettings.fixedParameters['e1']
        self.w2 = surrogateModelSettings.fixedParameters['w2']
        self.e2 = surrogateModelSettings.fixedParameters['e2']
        self.w3 = surrogateModelSettings.fixedParameters['w3']
        self.e3 = surrogateModelSettings.fixedParameters['e3']

    # Only overwrite variable weights
    def setVariableWeights(self, localsAtStart_dict):
        if 'w1' in localsAtStart_dict:
            self.w1 = localsAtStart_dict['w1']
        if 'e1' in localsAtStart_dict:
            self.e1 = localsAtStart_dict['e1']
        if 'w2' in localsAtStart_dict:
            self.w2 = localsAtStart_dict['w2']
        if 'e2' in localsAtStart_dict:
            self.e2 = localsAtStart_dict['e2']
        if 'w3' in localsAtStart_dict:
            self.w3 = localsAtStart_dict['w3']
        if 'e3' in localsAtStart_dict:
            self.e3 = localsAtStart_dict['e3']

