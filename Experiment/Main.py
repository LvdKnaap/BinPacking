from Experiment.SurrogateModel import *

from Settings.CustomSettings import *
from Settings.BinPackingSettings import *
from Settings.LocalSearchSettings import *
from Settings.SurrogateModelSettings import *


customSettings, localSearchSettings, surrogateModelSettings, binPackingSettings = \
    CustomSettings(), LocalSearchSettings(), SurrogateModelSettings(), BinPackingSettings()


if surrogateModelSettings.BO:
    surrogateModel = BayesianSurrogateModel(surrogateModelSettings, localSearchSettings,
                                            customSettings, binPackingSettings).solve(surrogateModelSettings)

# if surrogateModelSettings.hyperOpt:
#     surrogateModel = HyperoptSurrogateModel(surrogateModelSettings, localSearchSettings,
#                                             customSettings, binPackingSettings)
#


# NO SURROGATE: JUST LOCAL SEARCH ON BIN PACKING
# binpackingBatch = BinPackingBatchCustom(binPackingSettings)
# solver = LocalSearch2(localSearchSettings)
# solver.setInitialWeights(localSearchSettings) # will not be updated by variable weights
# for i in range(binPackingSettings.batchSize):
#     solver.solve(binpackingBatch.instances[i], customSettings.timeLimit)
