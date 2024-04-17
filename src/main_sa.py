
import cortisolDecadesOneDay as cdd
import time
from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.test_functions import Ishigami
import numpy as np


def citokynes(ktc,kmtc):
  parameters = [ktc,kmtc]
  simulation = 'F'
  output = cdd.cortisolDecadesOneDay(simulation, parameters,
                                 cortisol_exp=2.32)
  [t_wcsa, outputs_wcsa] = output
  [out_A, out_MA, out_MR, out_IL10, out_IL6, out_IL8, out_TNF, out_COR] = outputs_wcsa
  return t_wcsa, out_IL6



if __name__ == "__main__":
    start = time.time()

    problem = {
        'num_vars': 2,
        'names': ['ktc', 'kmtc'],
        'bounds': [[2.43, 4.43],
                  [1.78, 3.78]]
    }

    param_values = saltelli.sample(problem, 1024)

    model = np.zeros([param_values.shape[0]])

    for i, X in enumerate(param_values):
        print("X", X)
        model[i] = evaluate_model(X)

    Si = sobol.analyze(problem, model)

    print(Si['S1'])

    #Si.plot()

    end = time.time()
    print(f"Time: {int(end - start)}s" )
    
    print('Simulation done. Bye!')
    ### save cortisol graph
    ##post_processing(out_filename)