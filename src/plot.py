import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class SensitivityPlotter:
    def __init__(self, filename='sensitivity_data.npz'):
        """
        Load sensitivity analysis data from file.
        
        Parameters:
        -----------
        filename : str, optional
            Name of the input file (default: 'sensitivity_data.npz')
        """
        # Load the data
        data = np.load(filename)
        self.S1_data = data['S1']
        self.S2_data = data['S2']
        self.ST_data = data['ST']
        self.names = data['names']
        
        # Create a mock sp object with analysis dictionary
        self.sp = type('', (), {})()
        self.sp.analysis = {
            'S1': self.S1_data,
            'S2': self.S2_data,
            'ST': self.ST_data
        }

    def filter_zero_sensitivity(self):
        """
        Filter out parameters with zero first-order sensitivity.
        Returns filtered data and indices of non-zero elements.
        """
        # Find indices where S1 is not zero (using small threshold for floating point)
        non_zero_indices = np.where(np.abs(self.S1_data) > 1e-10)[0]
        
        # Create filtered versions of the data
        filtered_sp = type('', (), {})()
        filtered_sp.analysis = {
            'S1': self.S1_data[non_zero_indices],
            'ST': self.ST_data[non_zero_indices],
            'S2': self.S2_data[non_zero_indices][:, non_zero_indices]  # Filter both dimensions for S2
        }
        
        filtered_names = self.names[non_zero_indices]
        
        return filtered_sp, filtered_names

    def plot_first_order_sensitivity(self, sp, names):
        plt.figure(figsize=(24, 12))
        S1_data = sp.analysis['S1']
        
        bar_color = 'lightsteelblue'
        bars = plt.bar(range(len(names)), S1_data, color=bar_color, width=0.5)
        
        plt.xticks(range(len(names)), names, rotation=45, ha='right', fontsize=11)
        plt.yticks(fontsize=11)
        plt.ylabel("Índice de Sensibilidade de Primeira Ordem (S1)", fontsize=13, labelpad=15)
        plt.title("Índices de Sensibilidade de Primeira Ordem por Parâmetro - Cortisol", 
                  fontsize=15, pad=30)
        plt.grid(True, alpha=0.3)
        
        for i, v in enumerate(S1_data):
            plt.text(i, v + 0.02, f'{v:.3f}', 
                    ha='center', 
                    va='bottom',
                    fontsize=10,
                    color='black',
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=2))
        
        plt.subplots_adjust(bottom=0.2, left=0.1, right=0.95, top=0.9)
        plt.savefig('cortisol_first_order_sensitivity.png', dpi=300, bbox_inches='tight', pad_inches=0.5)
        plt.close()

    def plot_total_sensitivity(self, sp, names):
        plt.figure(figsize=(24, 12))
        ST_data = sp.analysis['ST']
        
        param_importance = list(zip(names, ST_data))
        param_importance.sort(key=lambda x: x[1], reverse=True)
        sorted_names, sorted_ST = zip(*param_importance)
        
        plt.bar(range(len(sorted_names)), sorted_ST, color='lightsteelblue', width=0.5)
        
        plt.xticks(range(len(sorted_names)), sorted_names, rotation=45, ha='right', fontsize=11)
        plt.yticks(fontsize=11)
        plt.ylabel("Índice de Sensibilidade Total (ST)", fontsize=13, labelpad=15)
        plt.title("Índices de Sensibilidade Total por Parâmetro - Cortisol", 
                  fontsize=15, pad=30)
        plt.grid(True, alpha=0.3)
        
        for i, v in enumerate(sorted_ST):
            plt.text(i, v + 0.02, f'{v:.3f}', 
                    ha='center', 
                    va='bottom',
                    fontsize=10,
                    color='black',
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=2))
        
        plt.subplots_adjust(bottom=0.2, left=0.1, right=0.95, top=0.9)
        plt.savefig('cortisol_total_sensitivity.png', dpi=300, bbox_inches='tight', pad_inches=0.5)
        plt.close()

    def plot_second_order_sensitivity(self, sp, names):
        plt.figure(figsize=(28, 18))
        S2_data = sp.analysis['S2']
        
        sns.heatmap(S2_data, 
                    xticklabels=names,
                    yticklabels=names,
                    cmap='YlOrRd',
                    annot=True,
                    fmt='.3f',
                    annot_kws={'size': 9},
                    cbar_kws={'label': 'Índice de Sensibilidade de Segunda Ordem (S2)',
                             'pad': 0.03})
        
        plt.title("Interações entre Parâmetros - Cortisol (Índices de Segunda Ordem)", 
                  fontsize=15, pad=30)
        
        plt.xticks(rotation=45, ha='right', fontsize=11)
        plt.yticks(rotation=0, fontsize=11)
        
        plt.subplots_adjust(left=0.15, bottom=0.15, right=0.95, top=0.95)
        plt.savefig('cortisol_second_order_sensitivity.png', dpi=300, bbox_inches='tight', pad_inches=0.5)
        plt.close()

    def create_all_plots(self, filter_zeros=False):
        """
        Create all three sensitivity plots using the loaded data.
        
        Parameters:
        -----------
        filter_zeros : bool, optional
            If True, only plot parameters with non-zero first-order sensitivity
            (default: False)
        """
        if filter_zeros:
            print("Filtering out parameters with zero first-order sensitivity...")
            plot_sp, plot_names = self.filter_zero_sensitivity()
            print(f"Plotting {len(plot_names)} parameters (filtered from {len(self.names)} total)")
        else:
            plot_sp = self.sp
            plot_names = self.names
        
        self.plot_first_order_sensitivity(plot_sp, plot_names)
        self.plot_total_sensitivity(plot_sp, plot_names)
        self.plot_second_order_sensitivity(plot_sp, plot_names)
        print("All plots created successfully!")

if __name__ == "__main__":
    plotter = SensitivityPlotter()
    # Para usar sem filtragem:
    # plotter.create_all_plots()
    # Para usar com filtragem:
    plotter.create_all_plots(filter_zeros=False)