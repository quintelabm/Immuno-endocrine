import cortisolDecadesOneDay as cdd
import time
from SALib import ProblemSpec
import numpy as np
import matplotlib.pyplot as plt
import math
import seaborn as sns

parametersDictionary = {
    'ktc': 3.43,
    'kmtc': 2.78,
    'kmct': 8.69,
    'kcd': 1.55,
    'klt': 3.35,
    'klt6': 1.20,
    'Cmax': 3,

    'n_106': 560,
    'n_610': 34.8,
    'n_66': 560,
    'n_6TNF': 185,
    'n_TNF6': 560,
    'n_810': 17.4,
    'n_8TNF':185,
    'n_M10': 4.35,
    'n_TNF10': 17.4,
    'n_MTNF': 0.1,
    'h_106': 3.68, 
    'h_610': 4,
    'h_66': 1,
    'h_6TNF': 2,
    'h_TNF6': 2,
    'h_810': 1.5,
    'h_8TNF': 3,
    'h_M10': 0.3,
    'h_TNF10': 3,
    'h_MTNF': 3.16,
    'k_106': 0.0191,
    'k_6': 4.64,
    'k_6m': 0.01,
    'k_6TNF': 0.81,
    'k_8': 0.464 ,
    'k_8m': 0.056,
    'k_8TNF': 0.56,
    'k_10': 1.1,
    'k_10m': 0.19,
    'k_TNF': 200,
    'k_TNFM': 1.5,   
    'k_MTNF': 8.65,
    'q_IL6': 0.6,
    'q_IL8': 0.2,
    'q_IL10': 0.15,
    'q_TNF': 0.14,

    'beta_A': 0.02,
    'k_A': 50,
    'm_A': 0.9,
    'k_m': 1.414,
}

def parametersInterval(parameters):
    bounds = []
    for param in parameters:
        bounds.append([parametersDictionary[param] - 0.1*parametersDictionary[param], 
                      parametersDictionary[param] + 0.1*parametersDictionary[param]])
    return bounds

def citokynes(cortisol_parameters, brady_parameters, quintela_parameters):
    simulation = 'F'
    output = cdd.cortisolDecadesOneDay(simulation, cortisol_parameters, brady_parameters, 
                                      quintela_parameters, cortisol_exp=2.32)
    [t_wcsa, outputs_wcsa] = output
    [out_A, out_MA, out_MR, out_IL10, out_IL6, out_IL8, out_TNF, out_COR] = outputs_wcsa
    
    size = np.size(out_COR)
    return out_COR[math.ceil(size/2)]

def plot_time_series(model_values):
    plt.figure(figsize=(20, 10))
    x = np.linspace(0, 24, len(model_values))
    
    plt.plot(x, model_values, label="Cortisol Médio", color='navy', linewidth=2)
    prediction_interval = 95
    plt.fill_between(x,
                    np.percentile(model_values, 50 - prediction_interval/2),
                    np.percentile(model_values, 50 + prediction_interval/2),
                    alpha=0.3, color='navy',
                    label=f"Intervalo de Predição {prediction_interval}%")
    
    plt.xlabel("Tempo (horas)", fontsize=13, labelpad=15)
    plt.ylabel("Concentração de Cortisol", fontsize=13, labelpad=15)
    plt.title("Variação do Cortisol ao longo de 24 horas", fontsize=15, pad=30)
    plt.legend(fontsize=11, loc='upper right', bbox_to_anchor=(0.95, 0.95))
    plt.grid(True, alpha=0.3)
    
    plt.xlim(0, 24)
    plt.xticks(np.arange(0, 25, 4), fontsize=11)
    plt.yticks(fontsize=11)
    
    plt.subplots_adjust(left=0.1, bottom=0.15, right=0.95, top=0.9)
    plt.savefig('cortisol_time_series.png', dpi=300, bbox_inches='tight', pad_inches=0.5)
    plt.close()

def save_sensitivity_data(S1_data, S2_data, ST_data, names, filename='sensitivity_data.npz'):
    """
    Save sensitivity analysis data and parameter names to a NPZ file.
    
    Parameters:
    -----------
    S1_data : array-like
        First order sensitivity indices
    S2_data : array-like
        Second order sensitivity indices
    ST_data : array-like
        Total sensitivity indices
    names : list
        Parameter names
    filename : str, optional
        Name of the output file (default: 'sensitivity_data.npz')
    """
    # Convert names list to numpy array for saving
    names_array = np.array(names, dtype=str)
    
    # Save all data in a single NPZ file
    np.savez(filename, 
             S1=S1_data,
             S2=S2_data,
             ST=ST_data,
             names=names_array)
    
    print(f"Data saved successfully to {filename}")

if __name__ == "__main__":
    start = time.time()

    names = ['ktc', 'kmtc', 'kmct', 'kcd', 'klt', 'klt6', 'Cmax', 'n_106', 'n_610', 
             'n_66', 'n_6TNF', 'n_TNF6', 'n_810', 'n_8TNF', 'n_M10', 'n_TNF10', 'n_MTNF', 'h_106', 'h_610', 
             'h_66', 'h_6TNF', 'h_TNF6', 'h_810', 'h_8TNF', 'h_M10', 'h_TNF10', 'h_MTNF', 'k_106', 'k_6', 'k_6m', 'k_6TNF', 'k_8', 'k_8m', 'k_8TNF', 'k_10', 'k_10m',
             'k_TNF',  'k_TNFM', 'k_MTNF', 'q_IL6', 'q_IL8', 'q_IL10', 'q_TNF']
    
    sp = ProblemSpec({
        "names": names,
        "groups": None,
        "bounds": parametersInterval(names),
        "outputs": ["Cortisol"],
    })

    sp.sample_sobol(1024, calc_second_order=True, seed=42)
    model_values = np.zeros(sp.samples.shape[0])

    for i, X in enumerate(sp.samples):
        [ktc, kmtc, kmct, kcd, klt, klt6, Cmax, n_106, n_610, n_66, n_6TNF, n_TNF6, n_810, n_8TNF, n_M10,
         n_TNF10, n_MTNF, h_106, h_610, h_66, h_6TNF, h_TNF6, h_810, h_8TNF, h_M10, h_TNF10, h_MTNF, k_106, k_6, 
         k_6m, k_6TNF, k_8, k_8m, k_8TNF, k_TNF, k_10, k_10m, k_TNFM, k_MTNF, q_IL6, q_IL8, q_IL10, q_TNF] = X

        cortisol_parameters = [ktc, kmtc, kmct, kcd, klt, klt6, Cmax]
        brady_parameters = [n_106, n_610, n_66, n_6TNF, n_TNF6, n_810, n_8TNF, n_M10, n_TNF10, n_MTNF, 
                          h_106, h_610, h_66, h_6TNF, h_TNF6, h_810, h_8TNF, h_M10, h_TNF10, h_MTNF, k_106, k_6, 
                          k_6m, k_6TNF, k_8, k_8m, k_8TNF, k_10, k_10m, k_TNF, k_TNFM, k_MTNF, q_IL6, q_IL8, q_IL10, q_TNF]
        quintela_parameters = []

        model_values[i] = citokynes(cortisol_parameters, brady_parameters, quintela_parameters)

    sp.set_results(model_values)
    sp.analyze_sobol(nprocs=4)

    # #The output can then be converted to a Pandas DataFrame for further analysis.
    # total_Si, first_Si, second_Si = sp.to_df()
    S1_data = sp.analysis['S1']
    S2_data = sp.analysis['S2']
    ST_data = sp.analysis['ST']

    save_sensitivity_data(S1_data, S2_data, ST_data, names)

    plot_time_series(model_values)
    # plot_first_order_sensitivity(sp, names)
    # plot_total_sensitivity(sp, names)
    # plot_second_order_sensitivity(sp, names)

    end = time.time()
    print(f"Tempo de execução: {int(end - start)}s")
    print('Simulação concluída!')