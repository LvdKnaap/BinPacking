# from hyperopt import fmin, tpe, space_eval
# from hyperopt import hp
import hyperopt as hyperopt

# define an objective function
def objective(args):
    case, val = args
    if case == 'case 1':
        return val
    else:
        return val ** 2

# define a search space
space = hyperopt.hp.choice('a',
    [
        ('case 1', 1 + hyperopt.hp.lognormal('c1', 0, 1)),
        ('case 2', hyperopt.hp.uniform('c2', -10, 10))
    ])


# minimize the objective over the space
best = hyperopt.fmin(objective, space, algo=hyperopt.tpe.suggest, max_evals=100)

print(best)
print(hyperopt.space_eval(space, best))