import hyperopt as hyperopt

class LocalSearchSettings:

    def __init__(self):

        #### START VARIABLE SETTINGS

        self.searchSpace_dict = {
                                 'w1': (-5, 5),
                                 'w3': (-3, 3),
                                 }

        self.pbounds_bo = self.searchSpace_dict # voor bo
        self.space_ho = {}
        for dimension in self.searchSpace_dict:
            self.space_ho[dimension] = hyperopt.hp.uniform(dimension, self.searchSpace_dict[dimension][0], self.searchSpace_dict[dimension][1])





        ##### START FIXED SETTINGS
        # if these are not included in th search space (ie 'bounds' or 'space') => use these values as fixed par.
        self.fixedParameters = {'w1': 10,
                                'w2': 0,
                                'w3': 1,
                                'e1': 1,
                                'e2': 1,
                                'e3': 1,
                                'temperatureReductionFactor': 0.99}


        # als < 0 dan wordtie genegeerd
        # self.customSeed = -1
        self.customSeed = 13

        self.simulatedAnnealing = False
        self.variableNeighborhoodSearch = True

        # neighborhoodrules either jointly or in isolation
        self.useMoveJoint = False
        self.useSwapJoint = False
        self.useMergeJoint = False
        self.useMoveIsolated = True
        self.useSwapIsolated = True
        self.useMergeIsolated = True

        # SA Settinggs
        self.initialTemperature = 10
        self.iterationsPerTemperatureReduction = 10
        # self.temperatureReductionFactor = 0.99
        self.evaluations = 0
        self.temperature = self.initialTemperature

        # VNS Settings
        self.minRandomWalks = 3
        self.maxRandomWalks = 6
        self.maxReduction = 10

        assert not(self.simulatedAnnealing and self.variableNeighborhoodSearch), "You cannot use Simulated Annealing AND Variable Neighborhood Search"