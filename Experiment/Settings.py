
class Settings:

    def __init__(self):

        ##### SETTINGS OWN METHOD
        self.timeLimit = 0.5 # in seconds
        self.weightSolvedInstances = 1
        self.weightTime = 0.1
        self.weightViolations = -0.1
        self.regularizationFactor = -0.002
        ###########################


        ##### BIN PACKING SETTINGS
        self.batchSizeType1 = 0
        self.batchSizeType2 = 0
        self.batchSizeType3 = 0
        self.batchSizeType4 = 10
        self.batchSizeType5 = 0
        self.batchSize = self.batchSizeType1 + self.batchSizeType2 + self.batchSizeType3 + self.batchSizeType4 + self.batchSizeType5
        ##########################


        ##### LOCAL SEARCH SETTINGS
        self.simulatedAnnealing = True
        ##########################



        ##### BAYESIAN OPTIMIZATION SETTINGS
        self.randomState = 13
        self.init_points = 3
        self.n_iter = 10
        self.acq = 'ucb'
        # self.alpha = 1e-2
        ###########################