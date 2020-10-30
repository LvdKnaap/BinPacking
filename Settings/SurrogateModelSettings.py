
class SurrogateModelSettings:

    def __init__(self):

        self.BO = True
        self.hyperOpt = False
        self.pbounds = {'w1': (-10, 10), 'w3': (-1, 3)}

        self.randomState = 13
        self.init_points = 3
        self.n_iter = 5
        self.acq = 'ucb'
        # self.alpha = 1e-2