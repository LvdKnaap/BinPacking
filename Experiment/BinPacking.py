import random as rd

class BinPackingBatchCustom:

    instances = []

    def __init__(self, binPackingSettings):
        self.instances = []

        for i in range(binPackingSettings.batchSizeType1):
            self.instances.append(BinPackingCustom(binPackingSettings.stepsize1*i+binPackingSettings.LB1, 1, binPackingSettings))
        for i in range(binPackingSettings.batchSizeType2):
            self.instances.append(BinPackingCustom(binPackingSettings.stepsize2*i+binPackingSettings.LB2, 2, binPackingSettings))
        for i in range(binPackingSettings.batchSizeType3):
            self.instances.append(BinPackingCustom(binPackingSettings.stepSize3*i+binPackingSettings.LB3, 3, binPackingSettings))
        for i in range(binPackingSettings.batchSizeType4):
            self.instances.append(BinPackingCustom(binPackingSettings.stepSize4*i+binPackingSettings.LB4, 4, binPackingSettings))
        for i in range(binPackingSettings.batchSizeType5):
            self.instances.append(BinPackingCustom(binPackingSettings.stepSize5*i+binPackingSettings.LB5, 5, binPackingSettings))
        for i in range(binPackingSettings.batchSizeType6):
            self.instances.append(BinPackingCustom(binPackingSettings.stepSize6*i+binPackingSettings.LB6, 6, binPackingSettings))


class BinPackingCustom:

    numBins = -1;
    numItems = -1;
    capacities = [];
    itemWeights = []
    numberOfConstraints = -1


    def __init__(self, numItems, type, binPackingSettings):
        self.numItems = numItems;
        self.itemWeights = []
        self.capacities = []
        self.binPackingSettings = binPackingSettings

        if type == 1: # standaard counter example voor greedy algorithms

            self.numBins = int(numItems/2);
            for i in range(self.numBins):
                self.capacities.append(10)

            if numItems % 2 == 1:
                print('aantal items is oneven. Onverwacht.')
            for i in range(numItems):
                if i % 2 == 0:
                    self.itemWeights.append(4)
                else:
                    self.itemWeights.append(6)

        elif type == 2: # partitioning problem met 2 bins en 5 items: {3, 7}^n; {2, 4, 4}^n, n = items/5
            self.numBins = 2

            for i in range(self.numBins):
                self.capacities.append(10*int(numItems/5))

            if numItems % 5 != 0:
                print('aantal items is geen meervoud van 5. Onverwacht.')
            for i in range(int(numItems/5)):
                self.itemWeights.append(2)
                self.itemWeights.append(3)
                self.itemWeights.append(4)
                self.itemWeights.append(4)
                self.itemWeights.append(7)

        elif type == 3: # 1 type is heel groot (even groot als bin). HOPELIJK is het in veel tussentijdse oplossingen
            #         handig om dat grote item aan geen bin toe te wijzen
            self.numBins = 2

            for i in range(self.numBins):
                self.capacities.append(numItems-1)

            self.itemWeights.append(self.capacities[0])
            for i in range(numItems-1):
                self.itemWeights.append(1)

        elif type == 4: #
            self.numBins = int(numItems/2)

            for i in range(self.numBins):
                self.capacities.append(10)

            self.itemWeights.append(self.capacities[0])
            for i in range(numItems - 1):
                self.itemWeights.append(1)

        elif type == 5: # random instances generator
            # momenteel: items krijgen unifrom int weight [1,4]. (dus average weight = 2.5)
                # bins = aantal items / 2 + 1 dus hopelijk voldoende ruimte
            self.numBins = int(numItems / 2) + 1

            rd.seed(13) # for consisntency
            for i in range(self.numBins):
                self.capacities.append(10)
            for i in range(numItems):
                self.itemWeights.append(rd.randint(1,4))


        elif type == 6:
            # type 6: N items, N bins, unieke item weights 1..N, unieke bin sizes 1..N.
            # Dus er bestaat maaar 1 oplossing: optimale solution moet er uit zien als identity matrix
            self.numBins = numItems
            for i in range(self.numBins):
                self.capacities.append(i+1)
            for i in range(numItems):
                self.itemWeights.append(i+1)
        else:
            print('undefined type')

        assert len(self.capacities) == self.numBins
        assert len(self.itemWeights) == self.numItems

        self.findNumberOfConstraints()


        if binPackingSettings.printInformation:
            print(self.numBins, 'bins', self.numItems, 'items')
            print('item weights: ', self.itemWeights)
            print('bin sizes: ', self.capacities)
            print()



    def evaluate(self, allocation, w1, e1, w2, e2, w3, e3):
        # allocations heeft items op rijen, bins op kolommen
        violationsPerType = []
        objective = 0

        # term 1. unassigned per item (boolean)
        violationsPerType.append(0)
        countUnassignedItems = 0

        for i in range(self.numItems):
            countThisItemAssigned = 0
            for j in range(self.numBins):
                if allocation[i][j]:
                    countThisItemAssigned += 1
            assert countThisItemAssigned <= 1, "error: 2x assigned. Dit is een hard constraint. Dit is niet de bedoeling!"

            # Check if the constraints is satisfied.
            if countThisItemAssigned == 0:
                countUnassignedItems += 1
                violationsPerType[0] += 1

        objective += w1 * countUnassignedItems ** e1


        # term 2. violated bin capacity per bin (amount / integer)
        violationsPerType.append(0)
        totalCapViolation = 0

        for j in range(self.numBins):
            violatedCapOfThisBin = -self.capacities[j]
            for i in range(self.numItems):
                if allocation[i][j]:
                    violatedCapOfThisBin += self.itemWeights[i]
            violatedCapOfThisBin = max(0, violatedCapOfThisBin)

            violationsPerType[1] += min(1, violatedCapOfThisBin)

            if violatedCapOfThisBin > 0:
                totalCapViolation += violatedCapOfThisBin

        objective += w2 * totalCapViolation ** e2

        # term 3. violated bin capacity per bin (boolean)
        if violationsPerType[1] > 0:
            objective += w3 * violationsPerType[1] ** e3

        # print(w1 * countUnassignedItems ** e1, w2 * totalPenaltyForCapViolation)

        maximumViolationsOverViolationTypes = max(violationsPerType)
        return [-1 * objective, maximumViolationsOverViolationTypes, violationsPerType, self.numberOfConstraints]


    def findNumberOfConstraints(self):
        self.numberOfConstraints = 0
        # The goal is to find the number of constraints that can be violated in 'violationsPerType'
        # number of unassigned items
        self.numberOfConstraints += self.numItems

        # maximum violated bin capacity
            # if all items in the smallest bin
        self.numberOfConstraints += sum(self.itemWeights) - min(self.capacities)
