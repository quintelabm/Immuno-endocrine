
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
  'klt6': 1.20,
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

  size = np.size(out_IL6)
  return out_IL6[math.ceil(size/2)]


if __name__ == "__main__":
    start = time.time()

    names = ['n_610', 'n_66', 'n_6TNF', 'n_MTNF', 'h_610', 'h_66', 'h_6TNF', 'h_MTNF', 'k_6', 'k_6m', 'k_6TNF', 'ktc', 'kmtc', 'kmct', 'klt6']
    problem = {
        'num_vars': np.size(names),
        'names': names,
        'bounds': parametersInterval(names)
    }

    param_values = saltelli.sample(problem, 1) #originalmente era 1024, coloquei 2 para rodar mais rápido
    model_values = np.zeros(param_values.shape[0])

    for i, X in enumerate(param_values):
        [n_610, n_66, n_6TNF, n_MTNF, h_610, h_66, h_6TNF, h_MTNF, k_6, k_6m, k_6TNF, ktc, kmtc, kmct, klt6] = X

        cortisol_parameters = [ktc, kmtc, kmct, klt6]
        brady_parameters = [n_610, n_66, n_6TNF, n_MTNF, h_610, h_66, h_6TNF, h_MTNF, k_6, k_6m, k_6TNF]
        quintela_parameters = []

        model_values[i] = citokynes(cortisol_parameters, brady_parameters, quintela_parameters)


    # print("S1: ", Si['S1'])
    # print("S2: ", Si['S2'])
    # print("ST: ", Si['ST'])

    # #The output can then be converted to a Pandas DataFrame for further analysis.
    # total_Si, first_Si, second_Si = Si.to_df()
    # # Note that if the sample was created with `calc_second_order=False`
    # # Then the second order sensitivities will not be returned
    # # total_Si, first_Si = Si.to_df()
  

    # #The output can then be converted to a Pandas DataFrame for further analysis.
    # total_Si, first_Si, second_Si = Si.to_df()
    # # Note that if the sample was created with `calc_second_order=False`
    # # Then the second order sensitivities will not be returned
    # # total_Si, first_Si = Si.to_df()

    # Si.heatmap()
    # plt.show()
  
    # barplot(total_Si)
    # filename = 'sobol_analysis_IL6_total.png'
    # plt.savefig(filename)

    # barplot(first_Si)
    # filename = 'sobol_analysis_IL6_first.png'
    # plt.savefig(filename)

    # barplot(second_Si)
    # filename = 'sobol_analysis_IL6_second.png'
    # plt.savefig(filename)


    # evaluate
    x = np.linspace(-1, 1, 100)
    y = np.array([parabola(*params) for params in param_values])

    print(np.size(y), np.size(x))

    # analyse
    sobol_indices = [ sobol.analyze(problem, model_values) for model_values in y.T]

    # Set up figure
    S1s = np.array([s['S1'] for s in sobol_indices])
    
    fig = plt.figure(figsize=(10, 6), constrained_layout=True)
    gs = fig.add_gridspec(2, 2)

    ax0 = fig.add_subplot(gs[:, 0])
    ax1 = fig.add_subplot(gs[0, 1])
    ax2 = fig.add_subplot(gs[1, 1])


    # Populate figure subplots
    for i, ax in enumerate([ax1, ax2]):
        ax.plot(x, S1s[:, i],
                label=r'S1$_\mathregular{{{}}}$'.format(problem["names"][i]),
                color='black')
        ax.set_xlabel("x")
        ax.set_ylabel("First-order Sobol index")

        ax.set_ylim(0, 1.04)

        ax.yaxis.set_label_position("right")
        ax.yaxis.tick_right()

        ax.legend(loc='upper right')

    ax0.plot(x, np.mean(y, axis=0), label="Mean", color='black')

    # in percent
    prediction_interval = 95

    ax0.fill_between(x,
                    np.percentile(y, 50 - prediction_interval/2., axis=0),
                    np.percentile(y, 50 + prediction_interval/2., axis=0),
                    alpha=0.5, color='black',
                    label=f"{prediction_interval} % prediction interval")

    ax0.set_xlabel("x")
    ax0.set_ylabel("y")

    plt.show()


    # Si.plot()
    # filename = 'sobol_analysis_IL6.png'
    # plt.savefig(filename)

    end = time.time()
    print(f"Time: {int(end - start)}s" )
    
    print('Simulation done. Bye!')
    ### save cortisol graph
    ##post_processing(out_filename)