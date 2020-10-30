import hyperopt as hyperopt

class SurrogateModelSettings:

    def __init__(self):

        self.BO = True
        self.hyperOpt = True

        #todo: een manier om input bounds automatisch goed te transformeren zodat de input goed is voor bo en hyperopt
        self.pbounds_bo = {'w1': (-10, 10), 'w3': (-1, 3)} # voor bo
        self.space_ho = { # voor hyperopt
            'w1': hyperopt.hp.uniform('w1', -10, 10),
            'w3': hyperopt.hp.uniform('w3', 1, 3),
        }

        # BAYESIAN OPTIMISATION SETTINGS
        self.randomState_bo = 13
        self.init_points_bo = 3
        self.n_iter_bo = 5
        self.acq_bo = 'ucb' # 'ei'
        # self.alpha = 1e-2


        # HYPEROPT SETTINGS
        self.algo_ho = 'hyperopt.tpe.suggest'
        self.max_evals_ho = 10