import uncertainpy as un
import numpy as np
import cortisolDecadesOneDay as cdd
import matplotlib.pyplot as plt
import chaospy as cp
import time
from collections import Counter

class CortisolModel(un.Model):
    def __init__(self):
        super(CortisolModel, self).__init__()
        
        # Contadores para debug
        self.error_counter = Counter()
        self.successful_runs = 0
        self.total_runs = 0
        
        # Definindo os parâmetros na ordem que deve ser passada para o modelo
        self.parameter_names = [
            'ktc', 'kmtc', 'kmct', 'kcd', 'klt', 'klt6', 'Cmax',  # cortisol_parameters
            'n_106', 'n_610', 'n_66', 'n_6TNF', 'n_TNF6', 'n_TNF10', 'n_MTNF',  # brady_parameters início
            'h_106', 'h_610', 'h_66', 'h_6TNF', 'h_TNF10', 'h_MTNF',
            'k_106', 'k_6', 'k_6m', 'k_6TNF', 'k_TNF', 'k_10', 'k_10m', 'k_TNFM',
            'q_IL10', 'q_TNF'  # brady_parameters fim
        ]
        
        self.parametersDictionary = {
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
            'n_M10': 4.35,
            'n_TNF10': 17.4,
            'n_MTNF': 0.1,
            'h_106': 3.68,
            'h_610': 4,
            'h_66': 1,
            'h_6TNF': 2,
            'h_TNF10': 3,
            'h_MTNF': 3.16,
            'k_106': 0.0191,
            'k_6': 4.64,
            'k_6m': 0.01,
            'k_6TNF': 0.81,
            'k_TNF': 200,
            'k_10': 1.1,
            'k_10m': 0.19,
            'k_TNFM': 1.5,
            'k_MTNF': 8.65,
            'q_IL6': 0.6,
            'q_IL10': 0.15,
            'q_TNF': 0.14,
        }
        
        self.fixed_t = np.linspace(0, 24, 1000)
        self.timeout = 300  # Aumentado para 5 minutos

    def run(self, **parameters):
        self.total_runs += 1
        start_time = time.time()
        
        # Debug: Imprimir parâmetros da iteração atual
        print(f"\nIteração {self.total_runs}")
        print("Parâmetros atuais:")
        for name, value in parameters.items():
            print(f"{name}: {value}")
        
        try:
            model_params = self.parametersDictionary.copy()
            model_params.update(parameters)
            
            # Garantindo a ordem correta dos parâmetros
            cortisol_parameters = [model_params[name] for name in self.parameter_names[:7]]
            brady_parameters = [model_params[name] for name in self.parameter_names[7:]]
            quintela_parameters = []

            # Verificar timeout
            if time.time() - start_time > self.timeout:
                self.error_counter['timeout'] += 1
                raise TimeoutError("Execução do modelo excedeu o tempo limite")

            output = cdd.cortisolDecadesOneDay('F', cortisol_parameters, brady_parameters, 
                                              quintela_parameters, cortisol_exp=2.32)
            
            t, outputs = output
            [_, _, _, _, _, _, _, out_COR] = outputs

            # Debug: Verificar valores antes da conversão
            print(f"Tamanho inicial dos dados - t: {len(t)}, out_COR: {len(out_COR)}")
            print(f"Valores únicos de cortisol: {len(set(out_COR))}")
            print(f"Range de valores: [{min(out_COR)}, {max(out_COR)}]")

            # Conversão para numpy arrays
            t = np.array(t).flatten()
            out_COR = np.array(out_COR).flatten()

            if len(t) > len(out_COR):
                print("Aviso: Ajustando comprimento de t")
                t = t[:len(out_COR)]
            elif len(out_COR) > len(t):
                print("Aviso: Ajustando comprimento de out_COR")
                out_COR = out_COR[:len(t)]

            # Ordenação
            sort_idx = np.argsort(t)
            t_sorted = t[sort_idx]
            cor_sorted = out_COR[sort_idx]

            # Remove valores não finitos
            valid_mask = np.isfinite(t_sorted) & np.isfinite(cor_sorted)
            t_clean = t_sorted[valid_mask]
            cor_clean = cor_sorted[valid_mask]
            
            print(f"Dados após limpeza - pontos válidos: {len(t_clean)}")

            # Verificar timeout novamente
            if time.time() - start_time > self.timeout:
                self.error_counter['timeout_late'] += 1
                raise TimeoutError("Execução do modelo excedeu o tempo limite após processamento")

            # Interpolação para ter 1000 pontos igualmente espaçados
            if len(t_clean) > 1:
                cor_interp = np.interp(self.fixed_t, t_clean, cor_clean)
                print(f"Interpolação bem-sucedida - valores únicos: {len(set(cor_interp))}")
            else:
                self.error_counter['interpolation_failed'] += 1
                print("Falha na interpolação - poucos pontos válidos")
                cor_interp = np.zeros_like(self.fixed_t)
            
            self.successful_runs += 1
            return self.fixed_t, cor_interp
            
        except TimeoutError as e:
            print(f"Timeout: {str(e)}")
            return self.fixed_t, np.zeros_like(self.fixed_t)
        except Exception as e:
            self.error_counter['other_error'] += 1
            print(f"Erro na execução do modelo: {str(e)}")
            print(f"Parâmetros que causaram o erro: {parameters}")
            return self.fixed_t, np.zeros_like(self.fixed_t)

def run_uncertainty_analysis():
    model = CortisolModel()
    
    # Selecionando apenas os parâmetros desejados para a análise
    selected_params = ['klt', 'kcd', 'kmtc', 'k_TNFM', 'Cmax', 'ktc']
    parameters = {}
    
    # Aumentando a variação dos parâmetros para ±10%
    for param_name in selected_params:
        nominal_value = model.parametersDictionary[param_name]
        min_value = nominal_value * 0.90  # -10%
        max_value = nominal_value * 1.10  # +10%
        parameters[param_name] = cp.Uniform(min_value, max_value)
    
    UQ = un.UncertaintyQuantification(
        model=model,
        parameters=parameters
    )
    
    # Ajustando os parâmetros do método de colocação
    data = UQ.quantify(
        seed=42,
        pc_method="collocation",
        polynomial_order=2,
        nr_collocation_points=10,
        nr_pc_mc_samples=1000,
        sa=True,
        plot="all"
    )
    
    # Imprimindo estatísticas de debug
    print("\n=== Estatísticas de Execução ===")
    print(f"Total de execuções: {model.total_runs}")
    print(f"Execuções bem-sucedidas: {model.successful_runs}")
    print("\nErros encontrados:")
    for error_type, count in model.error_counter.items():
        print(f"{error_type}: {count}")
    
    plot_uncertainty_results(data)
    return data, model

def plot_uncertainty_results(data):
    feature_name = "CortisolModel"
    feature_data = data[feature_name]
    
    plt.figure(figsize=(10, 6))
    
    t = feature_data.time
    mean = feature_data.mean
    p5 = feature_data.percentile_5
    p95 = feature_data.percentile_95

    print(f"Valores únicos de média: {len(set(mean))}", mean)
    
    # Debug: Imprimir estatísticas dos dados
    print("\n=== Estatísticas dos Resultados ===")
    print(f"Média dos valores médios: {np.mean(mean):.4f}")
    print(f"Desvio padrão dos valores médios: {np.std(mean):.4f}")
    print(f"Variação total (max-min) da média: {np.max(mean) - np.min(mean):.4f}")
    print(f"Variação média do intervalo de confiança: {np.mean(p95 - p5):.4f}")
    
    plt.plot(t, mean, color='#2c3e50', lw=2, label='Média')
    plt.fill_between(t, p5, p95, color='#3498db', alpha=0.3, label='Intervalo 90%')
    
    plt.title('Quantificação de Incerteza do Cortisol Circadiano', fontsize=14)
    plt.xlabel('Tempo (horas)', fontsize=12)
    plt.ylabel('Cortisol (µg/dL)', fontsize=12)
    plt.legend(loc='upper right')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xlim(0, 24)
    plt.xticks(np.arange(0, 25, 4))
    
    plt.tight_layout()
    plt.savefig('incerteza_cortisol.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\n=== Resultados da Quantificação de Incerteza ===")
    print(f"Média do pico circadiano: {np.max(mean):.2f} µg/dL")
    print(f"Amplitude média do intervalo de confiança: {np.mean(p95 - p5):.2f} µg/dL")
    print(f"Variância máxima: {np.max(feature_data.variance):.4f} (µg/dL)²")

if __name__ == "__main__":
    data, model = run_uncertainty_analysis()