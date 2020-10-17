from BinPacking2 import *
from LocalSearch2 import *
import random as rd
import numpy as np
import time


batchSizeType1 = 0
batchSizeType2 = 0
batchSizeType3 = 0
batchSizeType4 = 0
batchSizeType5 = 15

timeLimit = 2

binpackingBatch = BinPackingBatchCustom(batchSizeType1, batchSizeType2, batchSizeType3, batchSizeType4, batchSizeType5)

for x in range(-6, -4):
    for y in range(-1, 1):
        solver = LocalSearch2(1, 1, 1, 2 ** x, 1, 1, 1, 2 ** y, 1)
        totalScore = 0

        batchSize = batchSizeType1 + batchSizeType2 + batchSizeType3 + batchSizeType4 + batchSizeType5
        instancesSolved = 0

        for i in range(batchSize):
            # print('info about instance:')
            # print(binpackingBatch.instances[i].numItems, binpackingBatch.instances[i].numBins, binpackingBatch.instances[i].itemWeights)
            #
            # print(); print('solution info:')
            solver.solve(binpackingBatch.instances[i], timeLimit)
            # print(solver.curr_solution)
            # print(solver.curr_solutionValue)
            if solver.curr_solutionValue == 0:
                instancesSolved += 1
        print(2 ** x, 2 ** y, instancesSolved)



# batchSizeType1 = 0
# batchSizeType2 = 0
# batchSizeType3 = 10
# timeLimit = 2
#
# binpackingBatch = BinPackingBatchCustom(batchSizeType1, batchSizeType2, batchSizeType3)
# solver = LocalSearch2(1, 1, 1, 100, 1, 1, 1)
# totalScore = 0
#
# batchSize = batchSizeType1 + batchSizeType2 + batchSizeType3
#
# for i in range(batchSize):
#     print('info about instance:')
#     print(binpackingBatch.instances[i].numItems, binpackingBatch.instances[i].numBins, binpackingBatch.instances[i].itemWeights)
#
#     print(); print('solution info:')
#     solver.solve(binpackingBatch.instances[i], timeLimit)
#     print(solver.curr_solution)
#     print(solver.curr_solutionValue)


