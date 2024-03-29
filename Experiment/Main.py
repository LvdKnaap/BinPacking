from Experiment.SurrogateModel import *

from Settings.CustomSettings import *
from Settings.BinPackingSettings import *
from Settings.LocalSearchSettings import *
from Settings.SurrogateModelSettings import *

# INITIALIZE
customSettings, localSearchSettings, surrogateModelSettings, binPackingSettings = \
    CustomSettings(), LocalSearchSettings(), SurrogateModelSettings(), BinPackingSettings()


#### DIT WAS EERST DE HELE MAIN CLASS
customSettings, localSearchSettings, surrogateModelSettings, binPackingSettings = \
    CustomSettings(), LocalSearchSettings(), SurrogateModelSettings(), BinPackingSettings()

if surrogateModelSettings.BO:
    surrogateModel = BayesianSurrogateModel(surrogateModelSettings, localSearchSettings,
                                            customSettings, binPackingSettings).solve(surrogateModelSettings)

if surrogateModelSettings.hyperOpt:
    surrogateModel = HyperoptSurrogateModel(surrogateModelSettings, localSearchSettings,
                                            customSettings, binPackingSettings)

