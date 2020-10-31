
class LocalSearchSettings:

    def __init__(self):

        self.simulatedAnnealing = True
        self.variableNeighborhoodSearch = False # TODO INCORPORATE
        # neighborhoodrules either jointly or in isolation
        self.jointNeighborhoodRules = False # TODO INCORPORATE

        self.useMove = True
        self.useSwap = True
        self.useMerge = True

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