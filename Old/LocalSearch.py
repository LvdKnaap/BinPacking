import numpy as np
import random as rd


class LocalSearch:
    # Local search rules:
    useMove = False
    useSwap = False
    useMerge = False

    # // weight parameters
    w1 = 0
    W1 = 0
    w2 = 0
    W2 = 0

    # stopping criteria:
    budget_evaluations = 0
    timeLimit = 0

    curr_solutionValue = False;
    curr_solution = 0;

    def __init__(self, useMove, useSwap, useMerge, w1, W1, w2, W2):
        self.useMove = useMove
        self.useSwap = useSwap
        self.useMerge = useMerge
        self.w1 = w1
        self.W1 = W1
        self.w2 = w2
        self.W2 = W2

    def solve(self, binPackingInstance):
        self.curr_solution = self.createInitialSolution(binPackingInstance)
        self.curr_solutionValue = binPackingInstance.evaluate(self.curr_solution, self.w1, self.W1, self.w2, self.W2)

        improved = True;
        while improved and self.curr_solutionValue != 0:
            improved = self.performOneIteration(binPackingInstance)

    def performOneIteration(self, binPackingInstance):
        return self.merge(binPackingInstance, self.curr_solution) # eerst merge, dan swap, dan move
        return False

    def merge(self, binPackingInstance, input_solution):
        if self.curr_solutionValue == 0:
            return False

        if self.useMerge == 1:
            binOrder1 = list(range(binPackingInstance.numBins))
            rd.shuffle(binOrder1)
            binOrder2 = list(range(binPackingInstance.numBins))
            rd.shuffle(binOrder2)

            for bin1 in binOrder1:
                for bin2 in binOrder2:
                    # // create new solution and put all items from bin2 in bin1
                    new_solution = np.copy(input_solution)
                    if np.isnan(new_solution).any() or np.isinf(new_solution).any():
                        print("hier gaat fout 3")
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
        if self.curr_solutionValue == 0:
            return False

        if self.useSwap == 1:
            itemOrder1 = list(range(binPackingInstance.numItems))
            rd.shuffle(itemOrder1)
            itemOrder2 = list(range(binPackingInstance.numItems))
            rd.shuffle(itemOrder2)
            for item1 in itemOrder1:
                for item2 in itemOrder2:
                    # create new solution
                    new_solution = np.copy(input_solution)
                    if np.isnan(new_solution).any() or np.isinf(new_solution).any():
                        print("hier gaat fout 1")

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
        if self.curr_solutionValue == 0:
            return False

        if self.useMove == 1:
            itemOrder = list(range(binPackingInstance.numItems))
            rd.shuffle(itemOrder)
            binOrder = list(range(binPackingInstance.numBins))
            rd.shuffle(binOrder)
            for i in itemOrder:
                for j in binOrder:
                    new_solution = np.copy(input_solution)
                    if np.isnan(new_solution).any() or np.isinf(new_solution).any():
                        print("hier gaat fout 2")
                    # remove assignment to order bins
                    for binIndex in range(binPackingInstance.numBins):
                        new_solution[i][binIndex] = False
                    # perform the move
                    new_solution[i][j] = True
                    # accept or not?
                    if binPackingInstance.evaluate(new_solution, self.w1, self.W1, self.w2, self.W2) > self.curr_solutionValue: # > because maximization
                        self.curr_solutionValue = binPackingInstance.evaluate(new_solution, self.w1, self.W1, self.w2, self.W2)
                        self.curr_solution = new_solution
                        return True
        else:
            if binPackingInstance.evaluate(input_solution, self.w1, self.W1, self.w2,
                                           self.W2) > self.curr_solutionValue:  # > because maximization
                self.curr_solutionValue = binPackingInstance.evaluate(input_solution, self.w1, self.W1, self.w2, self.W2)
                self.curr_solution = input_solution
                return True
        return False




    def createInitialSolution(self, binPackingInstance):
        # Each item in bin 1
        initialSolution = np.zeros((binPackingInstance.numItems, binPackingInstance.numBins))
        for i in range(binPackingInstance.numItems):
            initialSolution[i][0] = 1
        return initialSolution