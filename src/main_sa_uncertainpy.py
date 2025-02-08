import cortisolDecadesOneDay as cdd
import time
import numpy as np
import os
import uncertainpy as un
import chaospy as cp
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# ======================================================================================
# PARÂMETROS DA SIMULAÇÃO (EDITÁVEIS)
# ======================================================================================
parametersDictionary = {
    # ----------------------------------------------------------------------------------
    # PARÂMETROS VARIÁVEIS (testados na análise de sensibilidade ±10%)
    # ----------------------------------------------------------------------------------
    'ktc': 3.43,        # [Cortisol] Magnitude da ativação do cortisol pelo TNF
    'kmtc': 2.78,       # [Cortisol] Meia-saturação para ativação do cortisol
    'k_6TNF': 0.81,     # [Brady] Taxa de upregulation de IL-6 por TNF
    
    # ----------------------------------------------------------------------------------
    # PARÂMETROS FIXOS (não variam na análise)
    # ----------------------------------------------------------------------------------
    # 'kmct': 8.69,     # [Cortisol] Meia-saturação para degradação de TNF (FIXO)
    # 'n_610': 34.8,    # [Brady] Meia-saturação de IL-6 por IL-10 (FIXO)
    # 'k_6m': 0.01,     # [Brady] Upregulation de IL-6 por macrófagos (FIXO)
}

# ======================================================================================
# CONFIGURAÇÃO DA ANÁLISE (EDITÁVEL)
# ======================================================================================
nr_samples = 50      # NÚMERO DE AMOSTRAS (cada amostra roda 1 vez o modelo) ⚠️ Altere aqui!
parallel = True      # Usar paralelismo (True = máximo desempenho)
seed = None          # None = mais rápido | 42 = resultados reproduzíveis


class CytokineModel(un.Model):
    def __init__(self):
        super().__init__()
        self.labels = list(parametersDictionary.keys())
        
    def run(self, **parameters):
        simulation = 'F'
        
        # ==============================================================================
        # PARÂMETROS FIXOS (não alterados na análise)
        # ==============================================================================
        cortisol_params = [
            parameters["ktc"],          # Variável
            parameters["kmtc"],         # Variável
            8.69,                       # kmct (FIXO)
            1.20                        # klt6 (FIXO)
        ]
        
        brady_params = [
            34.8,                       # n_610 (FIXO)
            560,                        # n_66 (FIXO)
            185,                        # n_6TNF (FIXO)
            0.1,                        # n_MTNF (FIXO)
            4,                          # h_610 (FIXO)
            1,                          # h_66 (FIXO)
            2,                          # h_6TNF (FIXO)
            3.16,                       # h_MTNF (FIXO)
            4.64,                       # k_6 (FIXO)
            0.01,                       # k_6m (FIXO)
            parameters["k_6TNF"]        # Variável
        ]
        
        quintela_params = [
            1.55,   # kcd (FIXO)
            3.35,   # klt (FIXO)
            3,      # Cmax (FIXO)
            8.65,   # k_MTNF (FIXO)
            0.6,    # q_IL6 (FIXO)
            0.02,   # beta_A (FIXO)
            50,     # k_A (FIXO)
            0.9,    # m_A (FIXO)
            1.414   # k_m (FIXO)
        ]

        try:
            output = cdd.cortisolDecadesOneDay(
                simulation,
                cortisol_params,
                brady_params,
                quintela_params,
                cortisol_exp=2.32
            )
            return output[0], output[1][4]  # Retorna (tempo, IL6)
        except:
            return None, np.nan


if __name__ == "__main__":
    start_time = time.time()
    
    # Configuração dos parâmetros variáveis
    parameters = un.Parameters({
        name: cp.Uniform(0.9 * value, 1.1 * value) 
        for name, value in parametersDictionary.items()
    })
    
    # Execução RÁPIDA
    UQ = un.UncertaintyQuantification(model=CytokineModel(), parameters=parameters)
    data = UQ.quantify(
        method="mc",
        nr_samples=nr_samples,      # ⚠️ Controla o número total de execuções!
        parallel=parallel,
        poolsize=os.cpu_count(),    # Usa TODOS os núcleos da CPU
        seed=seed
    )
    
    # ==================================================================================
    # GERAR GRÁFICOS
    # ==================================================================================
    # Gráfico de Sensibilidade (Sobol Total)
    sobol = data.sobol()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(parametersDictionary.keys()), y=sobol["IL6"].sobol_total, palette="rocket")
    plt.title(f"Sensibilidade dos Parâmetros (n={nr_samples} amostras)", fontsize=14)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('./Output/Graficos/sensibilidade.png', dpi=300)
    plt.show()

    # Gráfico de Dispersão (Relação Parâmetros vs IL6)
    df = pd.DataFrame(data.parameters)
    df["IL6"] = data["IL6"].evaluate
    sns.pairplot(df, diag_kind='kde', plot_kws={'alpha': 0.5})
    plt.suptitle("Relação entre Parâmetros e IL-6", y=1.02)
    plt.tight_layout()
    plt.savefig('./Output/Graficos/dispersao.png', dpi=300)
    plt.show()

    print(f"Tempo total: {(time.time() - start_time):.2f} segundos")
    print(f"Número total de execuções do modelo: {nr_samples}")