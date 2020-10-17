import random

class BinPacking:

    numBins = 0;
    numItems = 0;
    capacity = 0;
    itemWeights = []


    def __init__(self, numItems, numBins, capacity, specialArtificialInstance):
        self.numBins = numBins;
        self.numItems = numItems;
        self.capacity = capacity;
        self.itemWeights = []
        if specialArtificialInstance:
            self.capacity = 10;
            if numItems % 4 != 0:
                print("Verkeerd aantal items voor dit type instance")
            for i in range(int(numItems/2)):
                self.itemWeights.append(4)
            for i in range(int(numItems/2)):
                self.itemWeights.append(6)

        else:
            for i in range(numItems):
                self.itemWeights.append(random.randint(1, int(capacity/3)))





    def evaluate(self, allocation, w1, W1, w2, W2):
        # items op rijen, bins op kolommen
        # 1. unassigned per item (boolean)
        objective = 0
        countUnassignedItems = 0
        for i in range(self.numItems):
            unassigned = True
            for j in range(self.numBins):
                if allocation[i][j]:
                    unassigned = False
            if unassigned:
                countUnassignedItems += 1

        if W1 == 1:
            objective += w1 * countUnassignedItems
        elif W1 == 2:
            objective += w1 * countUnassignedItems ** 2
        else:
            print('error: to do implement W1 > 2')
            objective += w1 * countUnassignedItems ** W1

        # 2. maximum violated bin capacity (over bins)
        # todo: DIT KLOPT NIET VOLGENS. KAN JE NIET EEN NEGATIEVE SCORE KRIJGEN OMDAT WE GEEN MAX(0, ....) DOEN????
        #          PAS AAN VOOR SAFETY OF TEST MET EEN INSTANCE DIE NIET TIGHT IS (som van item sizes past precies in een bin....)
        maxViolatedCapacity = 0
        for j in range(self.numBins):
            violatedCapOfThisBin = -self.capacity
            for i in range(self.numItems):
                if allocation[i][j]:
                    violatedCapOfThisBin += self.itemWeights[i]
            maxViolatedCapacity = max(maxViolatedCapacity, violatedCapOfThisBin)

        if W2 == 1:
            objective += w2 * maxViolatedCapacity
        elif W2 == 2:
            objective += w2 * maxViolatedCapacity ** 2
        else:
            print('error: TO DO: implement W2 > 2')
            objective += w2 * maxViolatedCapacity ** W2

        return -1 * objective
