
class BinPackingSettings:

    def __init__(self):
        ##### BIN PACKING SETTINGS
        self.printInformation = False
        self.batchSizeType1 = 10
        self.batchSizeType2 = 0
        self.batchSizeType3 = 0
        self.batchSizeType4 = 0
        self.batchSizeType5 = 0
        self.batchSize = self.batchSizeType1 + self.batchSizeType2 + self.batchSizeType3 + self.batchSizeType4 + self.batchSizeType5

        self.LB1 = 6
        self.stepsize1 = 2
        self.LB2 = 5
        self.stepsize2 = 5
        self.LB3 = 50
        self.stepSize3 = 10
        self.LB4 = 20
        self.stepSize4 = 2
        self.LB5 = 10
        self.stepSize5 = 1
        ##########################
