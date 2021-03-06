import random as rd

class BinPackingBatchCustom:

    instances = []

    def __init__(self, numberOfInstancesType1, numberOfInstancesType2, numberOfInstancesType3, numberOfInstancesType4, numberOfInstancesType5):
        # (some sort of) lower bounds on instance sizes
        LB1 = 3 # (multiplied by 2)
        LB2 = 2 # (multiplied by 5)
        LB3 = 50
        stepSize3 = 10
        LB4 = 20
        stepSize4 = 2
        LB5 = 10
        stepSize5 = 1
        self.instances = []
        for i in range(numberOfInstancesType1):
            self.instances.append(BinPackingCustom(2*(i+LB1), 1)) # i+3 zorgt voor lower bound, kleine instances zijn té makkelijk
        for i in range(numberOfInstancesType2):
            self.instances.append(BinPackingCustom(5*(i+LB2), 2)) # i+3 zorgt voor lower bound, kleine instances zijn té makkelijk
        for i in range(numberOfInstancesType3):
            self.instances.append(BinPackingCustom(stepSize3*i+LB3, 3))
        for i in range(numberOfInstancesType4):
            self.instances.append(BinPackingCustom(stepSize4*i+LB4, 4))
        for i in range(numberOfInstancesType5):
            self.instances.append(BinPackingCustom(stepSize5*i+LB5, 5))



class BinPackingCustom:

    numBins = 0;
    numItems = 0;
    capacity = 0;
    itemWeights = []


    def __init__(self, numItems, type):
        self.numItems = numItems;
        self.itemWeights = []

        if type == 1: # standaard counter example voor greedy algorithms
            self.capacity = 10;
            self.numBins = int(numItems/2);
            if numItems % 2 == 1:
                print('aantal items is oneven. Onverwacht.')
            for i in range(numItems):
                if i % 2 == 0:
                    self.itemWeights.append(4)
                else:
                    self.itemWeights.append(6)

        elif type == 2: # partitioning problem met 2 bins en 5 items: {3, 7}^n; {2, 4, 4}^n, n = items/5
            self.capacity = 10*int(numItems/5);
            self.numBins = 2
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
            self.capacity = numItems-1
            self.numBins = 2

            self.itemWeights.append(self.capacity)
            for i in range(numItems-1):
                self.itemWeights.append(1)

        elif type == 4: #
            self.capacity = 10
            self.numBins = int(numItems/2)

            self.itemWeights.append(self.capacity)
            for i in range(numItems - 1):
                self.itemWeights.append(1)

        elif type == 5: # random instances generator
            # TODO: moet beter (iig moet het werken voor step size 1)
            # momenteel: items krijgen unifrom int weight [1,4]. (dus average weight = 2.5)
                # bins = aantal items / 2 + 1 dus hopelijk voldoende ruimte

            rd.seed(13) # for consisntency
            self.numBins = int(numItems/2) + 1
            self.capacity = 10
            for i in range(numItems):
                self.itemWeights.append(rd.randint(1,4))



        else:
            print('undefined type')



    def evaluate(self, allocation, w1, e1, w2, e2, w3, e3):
        # allocations heeft items op rijen, bins op kolommen
        violationsPerType = []
        objective = 0

        # 1. unassigned per item (boolean)
        violationsPerType.append(0)
        countUnassignedItems = 0

        for i in range(self.numItems):
            countThisItemAssigned = 0
            # unassigned = True
            for j in range(self.numBins):
                if allocation[i][j]:
                    countThisItemAssigned += 1
                    # if not unassigned:
                    #     print('error: 2x assigned. Dit is een hard constraint. Dit is niet de bedoeling!')
                    # else:
                    #     unassigned = False
            if countThisItemAssigned > 1:
                print('error: 2x assigned. Dit is een hard constraint. Dit is niet de bedoeling!')
            elif countThisItemAssigned == 0:
            # if unassigned:
                countUnassignedItems += 1
                violationsPerType[0] += 1

        objective += w1 * countUnassignedItems ** e1

        # 2. maximum violated bin capacity (over bins)
        violationsPerType.append(0)
        # TODO: is het w1 * \sum ( TERM ) ^ e1 of
        #     w1 * (\sum (TERM)) ^ e1 ?
        # ik doe nu de eerste
        totalPenaltyForCapViolation = 0
        for j in range(self.numBins):
            violatedCapOfThisBin = -self.capacity
            for i in range(self.numItems):
                if allocation[i][j]:
                    violatedCapOfThisBin += self.itemWeights[i]
            violatedCapOfThisBin = max(0, violatedCapOfThisBin)

            violationsPerType[1] += min(1, violatedCapOfThisBin)

            if violatedCapOfThisBin > 0:
                totalPenaltyForCapViolation += violatedCapOfThisBin ** e2

        objective += w2 * totalPenaltyForCapViolation

        if violationsPerType[1] > 0: ## number of bins that violated their cap
            objective += w3 * violationsPerType[1] ** e3




        maximumViolationsOverViolationTypes = max(violationsPerType)

        # print(w1 * countUnassignedItems ** e1, w2 * totalPenaltyForCapViolation)
        return [-1 * objective, maximumViolationsOverViolationTypes]
