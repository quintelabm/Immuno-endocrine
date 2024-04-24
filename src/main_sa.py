
import cortisolDecadesOneDay as cdd
import time
from SALib.sample import saltelli
from SALib.analyze import sobol
import numpy as np
import matplotlib.pyplot as plt
import math

parametersDictionary = {
  'ktc': 3.43,
  'kmtc': 2.78,
  'kmct': 8.69,
  'kcd': 1.55,
  'klt': 3.35,
  'klt6': 1.35, #da erro pra rodar a SA
  'Cmax': 3,

  'n_610': 34.8,
  'n_66': 560,
  'n_6TNF': 185,
  'n_M10': 4.35, #da erro pra rodar a SA
  'n_MTNF': 0.1,
  'h_610': 4,
  'h_66': 1,
  'h_6TNF': 2,
  'h_MTNF': 3.16,
  'k_6': 4.64,
  'k_6m': 0.01,
  'k_6TNF': 0.81,
  'k_MTNF': 8.65, #da erro pra rodar a SA
  'q_IL6': 0.6, #da erro pra rodar a SA

  'beta_A': 0.02, #da erro pra rodar a SA
  'k_A':50, #da erro pra rodar a SA
  'm_A': 0.9, #da erro pra rodar a SA
  'k_m': 1.414, #da erro pra rodar a SA
}

def parametersInterval(parameters):
  bounds = []
  for param in parameters:
    bounds.append([parametersDictionary[param] - 0.1*parametersDictionary[param], parametersDictionary[param] + 0.1*parametersDictionary[param]])
  return bounds





def citokynes(cortisol_parameters, brady_parameters, quintela_parameters):
  simulation = 'F'

  output = cdd.cortisolDecadesOneDay(simulation, cortisol_parameters, brady_parameters, quintela_parameters, cortisol_exp=2.32)

  [t_wcsa, outputs_wcsa] = output
  [out_A, out_MA, out_MR, out_IL10, out_IL6, out_IL8, out_TNF, out_COR] = outputs_wcsa

  #nenhum parametro do out_A funcionou na SA

  size = np.size(out_MA)
  return out_MA[math.ceil(size/2)]


if __name__ == "__main__":
    start = time.time()

    names = ['n_610', 'n_66', 'n_6TNF', 'n_MTNF', 'h_610', 'h_66', 'h_6TNF', 'h_MTNF', 'k_6', 'k_6m', 'k_6TNF', 'ktc', 'kmtc', 'kmct']
    problem = {
        'num_vars': np.size(names),
        'names': names,
        'bounds': parametersInterval(names)
    }

    param_values = saltelli.sample(problem, 1) #originalmente era 1024, coloquei 2 para rodar mais rápido
    model_values = np.zeros(param_values.shape[0])

    for i, X in enumerate(param_values):
        [n_610, n_66, n_6TNF, n_MTNF, h_610, h_66, h_6TNF, h_MTNF, k_6, k_6m, k_6TNF, ktc, kmtc, kmct] = X

        cortisol_parameters = [ktc, kmtc, kmct]
        brady_parameters = [n_610, n_66, n_6TNF, n_MTNF, h_610, h_66, h_6TNF, h_MTNF, k_6, k_6m, k_6TNF]
        quintela_parameters = []

        model_values[i] = citokynes(cortisol_parameters, brady_parameters, quintela_parameters)

    Si = sobol.analyze(problem, model_values)

    print("S1: ", Si['S1'])
    print("S2: ", Si['S2'])
    print("ST: ", Si['ST'])

    #The output can then be converted to a Pandas DataFrame for further analysis.
    total_Si, first_Si, second_Si = Si.to_df()
    # Note that if the sample was created with `calc_second_order=False`
    # Then the second order sensitivities will not be returned
    # total_Si, first_Si = Si.to_df()
  
    Si.plot()
    filename = 'sobol_analysis_MA.png'
    plt.savefig(filename)

    end = time.time()
    print(f"Time: {int(end - start)}s" )
    
    print('Simulation done. Bye!')
    ### save cortisol graph
    ##post_processing(out_filename)