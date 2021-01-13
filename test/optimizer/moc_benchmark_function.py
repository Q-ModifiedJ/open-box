import numpy as np
import math
from copy import deepcopy

from litebo.utils.config_space import ConfigurationSpace, UniformFloatHyperparameter
from platypus import NSGAII, Problem, Real


# === benchmark 1: bc with constraints
def branin(x1):
    x = deepcopy(x1)
    x = np.asarray(x)
    assert x.shape == (2,)
    x[0] = 15 * x[0] - 5
    x[1] = 15 * x[1]
    return float(
        np.square(x[1] - (5.1 / (4 * np.square(math.pi))) * np.square(x[0]) + (5 / math.pi) * x[0] - 6) + 10 * (
                1 - (1. / (8 * math.pi))) * np.cos(x[0]) + 10)


def Currin(x):
    x = np.asarray(x)
    assert x.shape == (2,)
    try:
        return float(((1 - math.exp(-0.5 * (1 / x[1]))) * (
                (2300 * pow(x[0], 3) + 1900 * x[0] * x[0] + 2092 * x[0] + 60) / (
                100 * pow(x[0], 3) + 500 * x[0] * x[0] + 4 * x[0] + 20))))
    except Exception as e:
        return 300


def get_setup_bc_c():
    # test scale
    # scale1 = [-100, 100]
    # scale2 = [0, 10]
    scale1 = [0, 1]
    scale2 = [0, 1]

    def multi_objective_func_bc_c(config):
        xs = config.get_dictionary()
        x0 = (xs['x0'] + scale1[0]) / (scale1[0] + scale1[1])
        x1 = (xs['x1'] + scale2[0]) / (scale2[0] + scale2[1])
        x = [x0, x1]  # x0, x1 in [0, 1]. test scale
        y1 = branin(x)
        y2 = Currin(x)
        c = (7 - y2, -y1)  # y2 >= 7, y1 >= 0
        res = dict()
        res['config'] = config
        res['objs'] = (y1, y2)
        MAXINT = 2 ** 31 - 1
        if any(ci > 0 for ci in c):
            res['objs'] = (MAXINT, MAXINT)
        res['constraints'] = c
        return res

    def get_cs_bc():
        cs_bc = ConfigurationSpace()
        x1 = UniformFloatHyperparameter("x0", scale1[0], scale1[1])
        # x1 = UniformIntegerHyperparameter("x0", scale1[0], scale1[1])  # test int
        x2 = UniformFloatHyperparameter("x1", scale2[0], scale2[1])
        cs_bc.add_hyperparameters([x1, x2])
        return cs_bc

    def run_nsgaii_bc_c():
        # Run NSGA-II to get 'real' pareto front
        def CMO(xi):
            xi = np.asarray(xi)
            y1 = Currin(xi)
            y2 = branin(xi)
            y = [y1, y2]
            y_c = [7 - y2, -y1]
            return y, y_c

        problem = Problem(2, 2, num_constraints)
        problem.types[:] = Real(0, 1)
        problem.constraints[:] = "<=0"
        problem.function = CMO
        algorithm = NSGAII(problem)
        algorithm.run(2500)
        cheap_pareto_front = np.array([list(solution.objectives) for solution in algorithm.result])
        cheap_constraints_values = [list(solution.constraints) for solution in algorithm.result]
        return cheap_pareto_front, cheap_constraints_values

    problem_str = 'bc-c'
    num_inputs = 2
    num_objs = 2
    num_constraints = 2
    referencePoint = [1e5] * num_objs   # must greater than max value of objective
    real_hv = 1e10

    setup = dict(
        multi_objective_func=multi_objective_func_bc_c,
        cs=get_cs_bc(),
        run_nsgaii=run_nsgaii_bc_c,
        problem_str=problem_str,
        num_inputs=num_inputs,
        num_objs=num_objs,
        num_constraints=num_constraints,
        referencePoint=referencePoint,
        real_hv=real_hv,
    )
    return setup


# === benchmark 2


# === benchmark 3
