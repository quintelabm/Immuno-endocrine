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

    'n_610': 34.8,
    'n_66': 560,
    'n_6TNF': 185,
    'n_M10': 4.35,
    'n_MTNF': 0.1,
    'h_610': 4,
    'h_66': 1,
    'h_6TNF': 2,
    'h_MTNF': 3.16,
    'k_6': 4.64,
    'k_6m': 0.01,
    'k_6TNF': 0.81,
    'k_MTNF': 8.65,
    'q_IL6': 0.6,

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
    plt.figure(figsize=(12, 6))
    # Converter para tempo em horas (24 horas)
    x = np.linspace(0, 24, len(model_values))
    
    plt.plot(x, model_values, label="IL-6 Média", color='navy', linewidth=2)
    prediction_interval = 95
    plt.fill_between(x,
                    np.percentile(model_values, 50 - prediction_interval/2),
                    np.percentile(model_values, 50 + prediction_interval/2),
                    alpha=0.3, color='navy',
                    label=f"Intervalo de Predição {prediction_interval}%")
    plt.xlabel("Tempo (horas)")
    plt.ylabel("Concentração de IL-6")
    plt.title("Variação da IL-6 ao longo de 24 horas")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Configurar eixo x para mostrar horas de 0 a 24
    plt.xlim(0, 24)
    plt.xticks(np.arange(0, 25, 4))  # Marcações a cada 4 horas
    
    plt.tight_layout()
    plt.savefig('il6_time_series.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_first_order_sensitivity(sp, names):
    plt.figure(figsize=(12, 6))
    S1_data = sp.analysis['S1']
    
    # Usar uma cor mais clara para as barras
    bar_color = 'lightsteelblue'
    
    # Criar gráfico de barras para S1
    bars = plt.bar(range(len(names)), S1_data, color=bar_color)
    plt.xticks(range(len(names)), names, rotation=45, ha='right')
    plt.ylabel("Índice de Sensibilidade de Primeira Ordem (S1)")
    plt.title("Índices de Sensibilidade de Primeira Ordem por Parâmetro")
    plt.grid(True, alpha=0.3)
    
    # Adicionar valores sobre as barras com fundo branco para melhor legibilidade
    for i, v in enumerate(S1_data):
        plt.text(i, v, f'{v:.3f}', 
                ha='center', 
                va='bottom',
                color='black',
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1)
                )
    
    plt.tight_layout()
    plt.savefig('il6_first_order_sensitivity.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_total_sensitivity(sp, names):
    plt.figure(figsize=(12, 6))
    ST_data = sp.analysis['ST']
    
    # Ordenar parâmetros por importância
    param_importance = list(zip(names, ST_data))
    param_importance.sort(key=lambda x: x[1], reverse=True)
    sorted_names, sorted_ST = zip(*param_importance)
    
    plt.bar(range(len(sorted_names)), sorted_ST, color='lightsteelblue')
    plt.xticks(range(len(sorted_names)), sorted_names, rotation=45, ha='right')
    plt.ylabel("Índice de Sensibilidade Total (ST)")
    plt.title("Índices de Sensibilidade Total por Parâmetro")
    plt.grid(True, alpha=0.3)
    
    # Adicionar valores sobre as barras
    for i, v in enumerate(sorted_ST):
        plt.text(i, v, f'{v:.3f}', 
                ha='center', 
                va='bottom',
                color='black',
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1)
                )
    
    plt.tight_layout()
    plt.savefig('il6_total_sensitivity.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_second_order_sensitivity(sp, names):
    plt.figure(figsize=(12, 10))
    S2_data = sp.analysis['S2']
    
    # Criar heatmap com valores numéricos
    sns.heatmap(S2_data, 
                xticklabels=names,
                yticklabels=names,
                cmap='YlOrRd',
                annot=True,
                fmt='.3f',
                cbar_kws={'label': 'Índice de Sensibilidade de Segunda Ordem (S2)'})
    
    plt.title("Interações entre Parâmetros (Índices de Segunda Ordem)")
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig('il6_second_order_sensitivity.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    start = time.time()

    names = ['n_610', 'n_66', 'n_6TNF', 'n_MTNF', 'h_610', 'h_66', 'h_6TNF', 
             'h_MTNF', 'k_6', 'k_6m', 'k_6TNF', 'ktc', 'kmtc', 'kmct', 'klt6']
    
    sp = ProblemSpec({
        "names": names,
        "groups": None,
        "bounds": parametersInterval(names),
        "outputs": ["Cortisol_Cytokines"],
    })

    sp.sample_sobol(4, calc_second_order=True)  # 1024 amostras
    model_values = np.zeros(sp.samples.shape[0])

    for i, X in enumerate(sp.samples):
        [n_610, n_66, n_6TNF, n_MTNF, h_610, h_66, h_6TNF, h_MTNF, k_6, k_6m, k_6TNF, ktc, kmtc, kmct, klt6] = X

        cortisol_parameters = [ktc, kmtc, kmct, klt6]
        brady_parameters = [n_610, n_66, n_6TNF, n_MTNF, h_610, h_66, h_6TNF, h_MTNF, k_6, k_6m, k_6TNF]
        quintela_parameters = []

        model_values[i] = citokynes(cortisol_parameters, brady_parameters, quintela_parameters)

    sp.set_results(model_values)
    sp.analyze_sobol(nprocs=4)

    # Gerar os gráficos separadamente
    plot_time_series(model_values)
    plot_first_order_sensitivity(sp, names)
    plot_total_sensitivity(sp, names)
    plot_second_order_sensitivity(sp, names)

    end = time.time()
    print(f"Tempo de execução: {int(end - start)}s")
    print('Simulação concluída!')