import hyperopt as hyperopt
import numpy as np

class SurrogateModelSettings:

    def __init__(self):

        self.BO = True
        self.hyperOpt = True

        # self.searchSpace_dict = {'w1': (-10, 10),
        #                          # 'w2': (1, 5),
        #                          'w3': (-1, 3),
        #                          # 'e1': (-5, 5),
        #                          # 'e2': (-5, 5),
        #                          # 'e3': (-5, 5),
        #                          }



        # if these are not included in th search space (ie 'bounds' or 'space') => use these values as fixed par.
        self.fixedParameters = {'w1': 10,
                                'w2': 1,
                                'w3': 1,
                                'e1': 1,
                                'e2': 1,
                                'e3': 1}


        #
        # self.pbounds_bo = self.searchSpace_dict # voor bo
        # self.space_ho = {}
        # for dimension in self.searchSpace_dict:
        #     self.space_ho[dimension] = hyperopt.hp.uniform(dimension, self.searchSpace_dict[dimension][0], self.searchSpace_dict[dimension][1])

        # BACKUP
        # self.space_ho = { # voor hyperopt
        #     'w1': hyperopt.hp.uniform('w1', -10, 10),
        #     'w3': hyperopt.hp.uniform('w3', 1, 3),
        # }

        self.randomState = 13

        # BAYESIAN OPTIMISATION SETTINGS
        self.printInformation_bo = True
        self.randomState_bo = self.randomState
        self.init_points_bo = 3
        self.n_iter_bo = 2
        self.acq_bo = 'ucb' # 'ei'
        # self.alpha = 1e-2


        # HYPEROPT SETTINGS
        self.printInformation_ho = True
        self.algo_ho = 'hyperopt.tpe.suggest'
        self.max_evals_ho = 5
        self.rstate_ho = np.random.RandomState(self.randomState)