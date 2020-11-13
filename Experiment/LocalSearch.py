import numpy as np
import random as rd
import time
import math



class LocalSearch2:
    # // weight parameters
    w1, e1, w2, e2, w3, e3 = -1, -1, -1, -1, -1, -1
    localSearchSettings = ""
    localSearchtype = ""

    # stopping criteria:
    budget_evaluations = 0
    timeLimit = 0
    startTime = 0
    solveTime = 0

    maximumViolationsOverViolationTypes = 0
    violationsPerType = []
    numberOfConstraints = 0

    curr_solutionValue = False;
    curr_solution = 0;

    currentlyInVNS = False


    def __init__(self, localSearchSettings):
        self.localSearchSettings = localSearchSettings
        rd.seed(localSearchSettings.customSeed)

        if localSearchSettings.simulatedAnnealing:
            self.localSearchtype = 'SA'
        elif localSearchSettings.variableNeighborhoodSearch:
            self.localSearchtype = 'VNS'
        else:
            self.localSearchtype = 'HC' # hill climbing



    def solve(self, binPackingInstance, timeLimit):
        self.curr_solution = self.createInitialSolution(binPackingInstance)
        # [self.curr_solutionValue, self.maximumViolationsOverViolationTypes, self.violationsPerType, self.numberOfConstraints] = binPackingInstance.evaluate(self.curr_solution, self.w1, self.e1, self.w2, self.e2, self.w3, self.e3)
        [self.curr_solutionValue, self.maximumViolationsOverViolationTypes, self.violationsPerType, self.numberOfConstraints] = binPackingInstance.evaluate(self.curr_solution, self)

        self.timeLimit = timeLimit
        self.startTime = time.time()

        improved = True;
        while improved and not self.shouldWeTerminate():
            improved = self.performOneIteration(binPackingInstance)

            if not improved and self.localSearchSettings.variableNeighborhoodSearch:
                # print('in a local optimum'); print(self.curr_solution);  print('starting VNS')
                self.currentlyInVNS = True
                numberOfWalks = rd.randint(self.localSearchSettings.minRandomWalks,
                                           self.localSearchSettings.maxRandomWalks)
                for shake in range(numberOfWalks):
                    self.performOneIteration(binPackingInstance)
                self.currentlyInVNS = False
                improved = True

        # register the end time
        self.solveTime = time.time() - self.startTime

        if binPackingInstance.binPackingSettings.printInformation:
            print('FINAL SOLUTION'); print(self.curr_solution); print(self.curr_solutionValue)


    def performOneIteration(self, binPackingInstance):
        neighboorhoodRules = self.randomizeNeighborhoodRules()
        improvedYet = False
        # print(); print();
        # print('before iteration:'); print(self.curr_solution)
        # print('volgorde rules: ', neighboorhoodRules)
        for neighboorhoodRule in neighboorhoodRules:
            if improvedYet:
                continue
            if not improvedYet and neighboorhoodRule == 'moveIso':
                improvedYet = self.moveIso(binPackingInstance)
                # if improvedYet:
                #     print('MOVED:'); print(self.curr_solution)
            if not improvedYet and neighboorhoodRule == 'swapIso':
                improvedYet = self.swapIso(binPackingInstance)
                # if improvedYet:
                #     print('SWAPPED'); print(self.curr_solution)
            if not improvedYet and neighboorhoodRule == 'mergeIso':
                improvedYet = self.mergeIso(binPackingInstance)
                # if improvedYet:
                #     print('MERGED'); print(self.curr_solution)
        return improvedYet
        # return self.merge(binPackingInstance, self.curr_solution) # eerst merge, dan swap, dan move
        # return False


    def randomizeNeighborhoodRules(self):
        neighboorhoodRules = []
        if self.localSearchSettings.useMoveIsolated:
            neighboorhoodRules.append('moveIso')
        if self.localSearchSettings.useSwapIsolated:
            neighboorhoodRules.append('swapIso')
        if self.localSearchSettings.useMergeIsolated:
            neighboorhoodRules.append('mergeIso')
        rd.shuffle(neighboorhoodRules)
        return neighboorhoodRules

    def moveIso(self, binPackingInstance):
        if self.shouldWeTerminate():
            return False

        itemOrder = list(range(binPackingInstance.numItems))
        binOrder = list(range(binPackingInstance.numBins+1)) # numBins+1 omdat we ook aan géén bin kunnen toewijzen

        rd.shuffle(itemOrder); rd.shuffle(binOrder)
        for i in itemOrder:
            for j in binOrder:
                new_solution = np.copy(self.curr_solution)
                # remove assignment to order bins
                for binIndex in range(binPackingInstance.numBins):
                    new_solution[i][binIndex] = False
                # perform the move
                if j < binPackingInstance.numBins: # stap 2 om te testen of we aan géén bin kunnen toewijzen
                    new_solution[i][j] = True

                # accept or not?
                if self.acceptOrNot(binPackingInstance, new_solution):
                    return True
        return False

    def swapIso(self, binPackingInstance):
        if self.shouldWeTerminate():
            return False

        itemOrder1 = list(range(binPackingInstance.numItems))
        itemOrder2 = list(range(binPackingInstance.numItems))

        rd.shuffle(itemOrder1); rd.shuffle(itemOrder2)

        for item1 in itemOrder1:
            for item2 in itemOrder2:
                if item1 == item2:
                    continue

                # create new solution
                new_solution = np.copy(self.curr_solution)

                oldBinItem1 = -1
                oldBinItem2 = -1
                for bin in range(binPackingInstance.numBins):
                    if new_solution[item1][bin]:
                        oldBinItem1 = bin
                    if new_solution[item2][bin]:
                        oldBinItem2 = bin

                # at least one of the two items is currently not assigned to a bin so they cannot be swapped
                if oldBinItem1 == -1 or oldBinItem2 == -1:
                    continue

                # perform swap
                new_solution[item1][oldBinItem1] = False
                new_solution[item2][oldBinItem2] = False
                new_solution[item1][oldBinItem2] = True
                new_solution[item2][oldBinItem1] = True

                # accept or not?
                if self.acceptOrNot(binPackingInstance, new_solution):
                    return True

        return False

    def mergeIso(self, binPackingInstance):
        if self.shouldWeTerminate():
            return False

        binOrder1 = list(range(binPackingInstance.numBins))
        binOrder2 = list(range(binPackingInstance.numBins))
        rd.shuffle(binOrder1); rd.shuffle(binOrder2)

        for bin1 in binOrder1:
            for bin2 in binOrder2:
                if bin1 == bin2:
                    continue
                # // create new solution and put all items from bin2 in bin1
                new_solution = np.copy(self.curr_solution)
                for i in range(binPackingInstance.numItems):
                    if new_solution[i][bin2]:
                        new_solution[i][bin2] = False
                        new_solution[i][bin1] = True

                # accept or not?
                if self.acceptOrNot(binPackingInstance, new_solution):
                    return True

        return False



    def acceptOrNot(self, binPackingInstance, new_solution):

        self.localSearchSettings.evaluations += 1

        # decrease temperature periodically
        if self.localSearchSettings.simulatedAnnealing and self.localSearchSettings.evaluations % self.localSearchSettings.iterationsPerTemperatureReduction == 0:
            self.localSearchSettings.temperature = self.localSearchSettings.temperatureReductionFactor * self.localSearchSettings.temperature;


        # always accept improvements:
        # if binPackingInstance.evaluate(new_solution, self.w1, self.e1, self.w2, self.e2, self.w3, self.e3)[0] > self.curr_solutionValue:  # > because maximizatione:
        if binPackingInstance.evaluate(new_solution, self)[0] > self.curr_solutionValue:  # > because maximizatione


            # [self.curr_solutionValue, self.maximumViolationsOverViolationTypes, self.violationsPerType, self.numberOfConstraints] = binPackingInstance.evaluate(
            #     new_solution, self.w1, self.e1, self.w2, self.e2, self.w3, self.e3)
            [self.curr_solutionValue, self.maximumViolationsOverViolationTypes, self.violationsPerType, self.numberOfConstraints] = binPackingInstance.evaluate(new_solution, self)
            self.curr_solution = new_solution
            # print('accepted because improvement', self.curr_solutionValue)
            return True

        # Simulated Annealing only
        elif self.localSearchSettings.simulatedAnnealing:
            # acceptProbability = math.exp((binPackingInstance.evaluate(new_solution, self.w1, self.e1, self.w2, self.e2, self.w3, self.e3)[0] - self.curr_solutionValue)/self.localSearchSettings.temperature)
            acceptProbability = math.exp((binPackingInstance.evaluate(new_solution, self)[0] - self.curr_solutionValue)/self.localSearchSettings.temperature)
            if rd.uniform(0, 1) < acceptProbability: # accept
                [self.curr_solutionValue, self.maximumViolationsOverViolationTypes, self.violationsPerType, self.numberOfConstraints] = binPackingInstance.evaluate(new_solution, self)
            #     [self.curr_solutionValue, self.maximumViolationsOverViolationTypes, self.violationsPerType, self.numberOfConstraints] = binPackingInstance.evaluate(
            #         new_solution, self.w1, self.e1, self.w2, self.e2, self.w3, self.e3)
                self.curr_solution = new_solution
                # print('accepted by SA', self.curr_solutionValue)
                return True

        # Variable Neighborhood Search only
        elif self.localSearchSettings.variableNeighborhoodSearch and self.currentlyInVNS:
            # accept if reduction in evaluation of the neigbhoor is smaller than maxReduction setting

            # if binPackingInstance.evaluate(new_solution, self.w1, self.e1, self.w2, self.e2, self.w3, self.e3)[
            if binPackingInstance.evaluate(new_solution, self)[
                0] + self.localSearchSettings.maxReduction > self.curr_solutionValue:  # > because maximizatione
                [self.curr_solutionValue, self.maximumViolationsOverViolationTypes, self.violationsPerType,
                 self.numberOfConstraints] = binPackingInstance.evaluate(new_solution, self)
                    # new_solution, self.w1, self.e1, self.w2, self.e2, self.w3, self.e3)
                self.curr_solution = new_solution
                # print('accepted because VNS', self.curr_solutionValue)
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
























































    def merge(self, binPackingInstance, input_solution):

        print('WE ARE USING JOINT NEIGHBOORHOOD RULES. THIS SHOULD PROBABLY BE LOOKED AT AGAIN. NOT DESIRABLE')

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

                    # at least one of the two items is currently not assigned to a bin so they cannot be swapped
                    if oldBinItem1 == -1 or oldBinItem2 == -1:
                        continue

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
        if self.shouldWeTerminate():
            return False

        if self.localSearchSettings.useMove == 1:
            itemOrder = list(range(binPackingInstance.numItems))
            rd.shuffle(itemOrder)
            # binOrder = list(range(binPackingInstance.numBins))
            binOrder = list(
                range(binPackingInstance.numBins + 1))  # stap 1 om te testen of we aan géén bin kunnen toewijzen
            rd.shuffle(binOrder)
            for i in itemOrder:
                for j in binOrder:
                    new_solution = np.copy(input_solution)
                    # remove assignment to order bins
                    for binIndex in range(binPackingInstance.numBins):
                        new_solution[i][binIndex] = False
                    # perform the move
                    if j < binPackingInstance.numBins:  # stap 2 om te testen of we aan géén bin kunnen toewijzen
                        new_solution[i][j] = True

                    # accept or not?
                    if self.acceptOrNot(binPackingInstance, new_solution):
                        return True
        else:
            # accept or not?
            if self.acceptOrNot(binPackingInstance, input_solution):
                return True
        return False
