import hyperopt as hyperopt
import numpy as np

class SurrogateModelSettings:

    def __init__(self):

        self.BO = True
        self.hyperOpt = True

        self.randomState = 13
        # self.randomState = 18
        # BAYESIAN OPTIMISATION SETTINGS
        self.printInformation_bo = True
        self.randomState_bo = self.randomState
        self.init_points_bo = 1
        self.n_iter_bo = 0
        # self.init_points_bo = 3
        # self.n_iter_bo = 97
        # self.n_iter_bo = 497
        self.acq_bo = 'ucb' # 'ei'
        # self.alpha = 1e-2


        # HYPEROPT SETTINGS
        self.printInformation_ho = True
        self.algo_ho = 'hyperopt.tpe.suggest'
        self.max_evals_ho = 5
        self.rstate_ho = np.random.RandomState(self.randomState)