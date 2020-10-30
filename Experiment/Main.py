from bayes_opt import BayesianOptimization
from BinPacking2 import *
from LocalSearch2 import *
import random as rd
import numpy as np
from Experiment.SurrogateModel import *
from Experiment.Settings import *


settings = Settings()



# INSTELLINGEN SURROGATE MODEL
pbounds = {'w1': (-10, 10), 'w3': (-1, 3)}



type = 'BO'
# EIND INSTELLINGEN SURROGATE MODEL
if type == 'BO':
    surrogateModel = BayesianSurrogateModel(pbounds, settings)
elif type == 'hyperopt':
    surrogateModel = HyperoptSurrogateModel()



# GOOOO
surrogateModel.solve(settings)
