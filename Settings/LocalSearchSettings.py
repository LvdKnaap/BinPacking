
class LocalSearchSettings:

    def __init__(self):

        self.simulatedAnnealing = True
        # self.useMove = True
        # self.useSwap = True
        # self.useMerge = True
        #
        # solver = LocalSearch2(1, 1, 1, 2 ** w1, 1, 1, 1, 2 ** w3, 1, localSearchSettings.simulatedAnnealing, 10, 10,
        #                       0.99)
        #
        # def __init__(self, useMove, useSwap, useMerge, w1, e1, w2, e2, w3, e3, simulatedAnnealing, initialTemperature,
        #              iterationsPerTemperatureReduction, temperatureReductionFactor):
        #     self.useMove = useMove
        #     self.useSwap = useSwap
        #     self.useMerge = useMerge
        #     self.w1 = w1
        #     self.e1 = e1
        #     self.w2 = w2
        #     self.e2 = e2
        #     self.w3 = w3
        #     self.e3 = e3
        #     self.simulatedAnnealing = simulatedAnnealing
        #     if self.simulatedAnnealing:
        #         self.initialTemperature = initialTemperature
        #         self.temperature = initialTemperature
        #         self.iterationsPerTemperatureReduction = iterationsPerTemperatureReduction
        #         self.temperatureReductionFactor = temperatureReductionFactor
        #         self.evaluations = 0