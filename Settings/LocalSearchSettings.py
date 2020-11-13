import hyperopt as hyperopt

class LocalSearchSettings:

    def __init__(self):

        #### START VARIABLE SETTINGS

        self.searchSpace_dict = {'w1': (-10, 10),
                                 # 'w2': (1, 5),
                                 'w3': (-1, 3),
                                 # 'e1': (-5, 5),
                                 # 'e2': (-5, 5),
                                 # 'e3': (-5, 5),
                                 # 'temperatureReductionFactor': (0, 1), # TODO: WERKT, WIL IK DIT OP DEZE MANIER VOOR ALLES?
                                 }

        self.pbounds_bo = self.searchSpace_dict # voor bo
        self.space_ho = {}
        for dimension in self.searchSpace_dict:
            self.space_ho[dimension] = hyperopt.hp.uniform(dimension, self.searchSpace_dict[dimension][0], self.searchSpace_dict[dimension][1])





        ##### START FIXED SETTINGS
        # if these are not included in th search space (ie 'bounds' or 'space') => use these values as fixed par.
        self.fixedParameters = {'w1': 10,
                                'w2': 1,
                                'w3': 1,
                                'e1': 1,
                                'e2': 1,
                                'e3': 1,
                                'temperatureReductionFactor': 0.99}


        self.customSeed = 13

        self.simulatedAnnealing = True
        self.variableNeighborhoodSearch = False

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