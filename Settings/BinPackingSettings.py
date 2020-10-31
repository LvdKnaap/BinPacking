
class BinPackingSettings:

    def __init__(self):
        ##### BIN PACKING SETTINGS
        self.batchSizeType1 = 2
        self.batchSizeType2 = 2
        self.batchSizeType3 = 2
        self.batchSizeType4 = 0
        self.batchSizeType5 = 2
        self.batchSize = self.batchSizeType1 + self.batchSizeType2 + self.batchSizeType3 + self.batchSizeType4 + self.batchSizeType5
        ##########################
