from openbox.benchmark.objective_functions.synthetic import Branin
from openbox.optimizer.generic_smbo import SMBO

branin = Branin()
bo = SMBO(branin.evaluate,      # objective function
          branin.config_space,  # config space
          num_objs=branin.num_objs,  # number of objectives
          num_constraints=branin.num_constraints,  # number of constraints
          max_runs=50,          # number of optimization rounds
          surrogate_type='prf',
          time_limit_per_trial=180,
          task_id='quick_start')
history = bo.run()
print(history)
