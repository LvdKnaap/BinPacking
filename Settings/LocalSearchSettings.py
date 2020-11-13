
class LocalSearchSettings:

    def __init__(self):

        self.customSeed = 13

        self.simulatedAnnealing = False
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
        self.temperatureReductionFactor = 0.99
        self.evaluations = 0
        self.temperature = self.initialTemperature

        # VNS Settings
        self.minRandomWalks = 3
        self.maxRandomWalks = 6
        self.maxReduction = 10

        assert not(self.simulatedAnnealing and self.variableNeighborhoodSearch), "You cannot use Simulated Annealing AND Variable Neighborhood Search"