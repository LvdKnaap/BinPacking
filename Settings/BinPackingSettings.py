
class BinPackingSettings:

    def __init__(self):
        ##### BIN PACKING SETTINGS
        self.batchSizeType1 = 0
        self.batchSizeType2 = 0
        self.batchSizeType3 = 0
        self.batchSizeType4 = 25
        self.batchSizeType5 = 0
        self.batchSize = self.batchSizeType1 + self.batchSizeType2 + self.batchSizeType3 + self.batchSizeType4 + self.batchSizeType5
        ##########################
