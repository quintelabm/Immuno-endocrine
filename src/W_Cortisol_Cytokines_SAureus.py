# -*- coding: utf-8 -*-
"""03_Cortisol+_Cytokines_SAureus.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Hw97rVuzIkmXQnOr3KIQK8Yh7tqXyCTz
"""

from scipy.integrate import odeint, solve_ivp
import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd
import csv

# Mathematical model of the immune response activation including cortisol and glucose dynamics
# Obs: All the rates are represented per day

# /*******************************************************************************
#  * @param y - equations of simulation
#  * @param t - evenly spaced array with time of simulation
#  * @param flag - 
#  * @param params - 
#  ******************************************************************************/
def f(t, y, flag, params):
     
     # Parameters by Brady et al., (2016):
     n_106 = 560            # pg/mL    # Half-maximum value associated with upregulation of IL-10 by IL-6
     n_610 = 34.8           # pg/mL    # Half-maximum value associated with downregulation of IL-6 by IL-10
     n_66 = 560             # pg/mL    # Half-maximum value associated with the auto-negative feedback of IL-6
     n_6TNF = 185           # pg/mL    # Half-maximum value associated with upregulation of IL-6 by TNF-a
     n_TNF6 = 560           # pg/mL    # Half-maximum value associated with downregulation of TNF-a by IL-6
     n_810 = 17.4           # pg/mL    # Half-maximum value associated with downregulation of IL-8 by IL-10
     n_8TNF = 185           # pg/mL    # Half-maximum value associated with upregulation of IL-8 by TNF-a
     n_M10 = 4.35           # pg/mL    # 
     n_TNF10 = 17.4         # pg/mL    # Half-maximum value associated with downregulation of TNF-a by IL-10
     n_MTNF = 0.1           # ?        #  
     h_106 = 3.68           # -        # Hill function exponent associated with upregulation of IL-10 by IL-6
     h_610 = 4              # -        # Hill function exponent associated with downregulation of IL-6 by IL-10
     h_66 = 1               # -        # Hill function exponent associated with auto-negative feedback of IL-6
     h_6TNF = 2             # -        # Hill function exponent associated with upregulation of IL-6 by TNF-a
     h_TNF6 = 2             # -        # Hill function exponent associated with downregulation of TNF-a by IL-6
     h_810 = 1.5            # -        # Hill function exponent associated with downregulation of IL-8 by IL-10
     h_8TNF = 3             # -        # Hill function exponent associated with upregulation of IL-8 by TNF-a
     h_M10 = 0.3            # -        # 
     h_TNF10 = 3            # -        # Hill function exponent associated with downregulation of TNF-a by IL-10
     h_MTNF = 3.16          # -        # 
     k_106 = 0.0191         # relative cytokine concentration/(day · # of cells)    # Upregulation of IL-10 by IL-6
     k_6 = 4.64             # day-1                                                 # Activation rate (per hour) of IL-6
     k_6m = 0.01            # relative cytokine concentration/(day · # of cells)    # Upregulation of IL-6 by the activated macrophages
     k_6TNF = 0.81          # relative cytokine concentration/(day · # of cells)    # Upregulation of IL-6 by TNF-a
     k_8 = 0.464            # day-1                                                 # Activation rate (per hour) of IL-8
     k_8m = 0.056           # relative cytokine concentration/(day · # of cells)    # Upregulation of IL-8 by the activated macrophages
     k_8TNF = 0.56          # relative cytokine concentration/(day · # of cells)    # Upregulation of IL-8 by TNF-a
     k_10 = 1.1             # day-1                                                 # Activation rate (per hour) of IL-10
     k_10m = 0.19           # relative cytokine concentration/(day · # of cells)    # Upregulation of IL-10 by the activated macrophages
     k_TNF = 200            # day–1                                                 # Activation rate (per hour) of TNF-a
     k_TNFM = 1.5           # relative cytokine concentration/(day · # of cells)    # Upregulation of TNF-a by the activated macrophages
     k_MTNF = 8.65          # hr-1                                                  # Activation rate of resting macrophages influenced by
     q_IL6 = 0.6            # relative concentration                                # The concentration of IL-6 in the absence of a pathogen
     q_IL8 = 0.2            # relative concentration                                # The concentration of IL-8 in the absence of a pathogen
     q_IL10 = 0.15          # relative concentration                                # The concentration of IL-10 in the absence of a pathogen
     q_TNF = 0.14           # relative concentration                                # The concentration of TNF-a in the absence of a pathogendescription

     # Cortisol parameters by Pritchard-Bell, Ari  (2016) - Best values
     ktc  = 3.43            # ng/(pg·h)                                             # The magnitude of cortisol activation by TNF
     kmct = 8.69            # ng/mL                                                 # 
     kmtc = 2.78            # pg/mL                                                 # 
     kcd  = 1.55            # h^-1                                                  # Cortisol degradation
     klt = 3.35             # h^-1
     Cmax = 3

     # Parameters by Quintela et al., (2014)
     beta_A = 0.02  # 1/day           # Replication rate of the bacteria
     k_A = 50.0     # mm^3/day        # Carrying capacity of the bacteria
     m_A = 0.9      # 1/day           # Phagocytosis of the bacteria
     MR_max = 5     # Macrophages resting max    
     k_MA = 2.51    #                 # Activated macrophage decay rate
     k_MR = 6       #                 # Resting macrophage decay rate 
     k_m = 1.414    #                 # Macrophage activation rate

     A = y[0]
     MA = y[1]
     MR = y[2]
     IL10 = y[3]
     IL6 = y[4]
     IL8 = y[5]
     TNF = y[6]
     COR = y[7]
     
     if flag == 0:
          gluc = 0
     else:
          #result_index = glucose[0].sub(t).abs().idxmin()
          closest_index = params['index'].sub(t).abs().idxmin()
          #print(result_index)  
          #glucose = pd.DataFrame(params[0])
          gluc = params.at[closest_index,'values']
          #print(gluc)

     dAdt = (beta_A * A *(1 - (A / k_A)) - m_A * A * MA)

     #dAdt_wo = (beta_A * A_wo *(1 - (A_wo / k_A)) - m_A * A_wo * MA)
     
     dMAdt = (k_m + k_MTNF * pow(TNF, h_MTNF) / (pow(n_MTNF, h_MTNF) + pow(TNF, h_MTNF)) * (pow(n_M10, h_M10) / (pow(n_M10, h_M10)\
               + pow(IL10, h_M10)))) * MR * A - k_MA * MA
     
     dMRdt = -(k_m + k_MTNF * (pow(TNF, h_MTNF) / (pow(n_MTNF, h_MTNF) + pow(TNF, h_MTNF))) * (pow(n_M10, h_M10) / (pow(n_M10, h_M10)\
               + pow(IL10, h_M10)))) * MR * A + k_MR * MR * (1 - MR / MR_max)
          
     dIL10dt = (k_10m + k_106 * (pow(IL6, h_106) / (pow(n_106, h_106) + pow(IL6, h_106)))) * MA \
                - k_10 * (IL10 - q_IL10)
     #added cortisol influence term: - klt*COR*(1-COR/(COR+kmct))
     dIL6dt = (k_6m + k_6TNF * (pow(TNF, h_6TNF) / (pow(n_6TNF, h_6TNF) + pow(TNF, h_6TNF))) * (pow(n_66, h_66) / (pow(n_66, h_66)\
               + pow(IL6, h_66))) * (pow(n_610, h_610) / (pow(n_610, h_610) + pow(IL10, n_610)))) * MA - klt*COR*(1-COR/(COR+kmct))\
                - k_6 * (IL6 - q_IL6)
     
     dIL8dt = (k_8m + k_8TNF * (pow(TNF, h_8TNF) / (pow(TNF, h_8TNF) + pow(n_8TNF, h_8TNF))) * (pow(n_810, h_810) / (pow(n_810, h_810)\
               + pow(IL10, h_810)))) * MA - k_8 * (IL8 - q_IL8)
     
     dTNFdt = (k_TNFM * (pow(n_TNF6, h_TNF6) / (pow(n_TNF6, h_TNF6) \
               + pow(IL6, h_TNF6))) * (pow(n_TNF10, h_TNF10) / (pow(n_TNF10, h_TNF10)\
               + pow(IL10, h_TNF10)))) * MA - klt*COR*(1-COR/(COR+kmct)) - k_TNF * (TNF - q_TNF)
     
     #dTNFdt = ((k_TNFM * (pow(n_TNF6, h_TNF6) / (pow(n_TNF6, h_TNF6) \
     #          + pow(IL6, h_TNF6))) * (pow(n_TNF10, h_TNF10) / (pow(n_TNF10, h_TNF10)\
     #         + pow(IL10, h_TNF10)))) * MA *klt*COR - k_TNF * (TNF - q_TNF))

     dCORdt = ktc * (TNF/(TNF + kmtc)) * (Cmax - COR) * gluc - kcd*COR     
     #dCORdt = ktc*TNF- kcd*COR

     return [dAdt, dMAdt, dMRdt, dIL10dt, dIL6dt, dIL8dt, dTNFdt, dCORdt]



# /*******************************************************************************
#  * @param flag - 
#  * @param params - 
#  * @param ic - 
#  ******************************************************************************/
def W_Cortisol_Cytokines_SAureus(flag, params, ic):
     '''
     # Initial Conditions by experimental data
     A = 2                  # Cell/mm3 # S. aureus Bacteria               
     MA = 5                 #  -       # Macrophages activated
     MR = 10                # Cell/mm3 # Macrophages resting
     IL_6 = 0               #          # Interleukin-6 (pro-inflammatory)
     IL_8 = 0               #          # Interleukin-8 (pro-inflammatory)
     IL_10 = 0.7            #          # Interleukin-10 (anti-inflammatory)
     TNF = 0.17             #          # Tumor Necrosis Factor a (pro-inflammatory)     
     COR = 1                #          # Test value to Cortisol
     '''
     A = ic[0]#2                  # Cell/mm3 # S. aureus Bacteria               
     MA = ic[1]#5                 #  -       # Macrophages activated
     MR = ic[2]#10                # Cell/mm3 # Macrophages resting
     IL_6 = ic[3]#0               #          # Interleukin-6 (pro-inflammatory)
     IL_8 = ic[4]#0               #          # Interleukin-8 (pro-inflammatory)
     IL_10 = ic[5]#0.7            #          # Interleukin-10 (anti-inflammatory)
     TNF = ic[6]#0.17             #          # Tumor Necrosis Factor a (pro-inflammatory)     
     COR = ic[7]#1                #          # Test value to Cortisol


     # Initial Conditions of Each Equation
     y0 = [A, MA, MR, IL_10, IL_6, IL_8, TNF, COR]
          
     # Simulation Parameters
     sim_time = 1           # day        # Total time of simulation in min 
     deltaT = pow(10, -3)   # -          # Step size
     t = np.arange(0,sim_time,deltaT)

     sol = solve_ivp(f, [0,sim_time], y0, args=(flag, params), t_eval=t)
     
     out_A = sol.y[0]
     out_MA = sol.y[1]
     out_MR = sol.y[2]
     out_IL10 = sol.y[3]
     out_IL6 = sol.y[4]
     out_IL8 = sol.y[5]
     out_TNF = sol.y[6]
     out_COR = sol.y[7]
     

     outputs = [out_A, out_MA, out_MR, out_IL10, out_IL6, out_IL8, out_TNF, out_COR]
     return [t, outputs]


def plots_w_c_sa(t, folder, outputs, day):

     [out_A, out_MA, out_MR, out_IL10, out_IL6, out_IL8, out_TNF, out_COR] = outputs

     # Normalization
     out_TNF = 100 * (out_TNF - min(out_TNF)) / (max(out_TNF) - min(out_TNF))
     out_IL6 = 100 * (out_IL6 - min(out_IL6)) / (max(out_IL6) - min(out_IL6))
     out_IL8 = 100 * (out_IL8 - min(out_IL8)) / (max(out_IL8) - min(out_IL8))
     out_IL10 = 100 * (out_IL10 - min(out_IL10)) / (max(out_IL10) - min(out_IL10))
     
     # Cytokines
     fig, (ax1) = plt.subplots(1,1)
     ax1.plot(t, out_TNF,'purple',  linewidth=3, label="TNF α")
     ax1.plot(t, out_IL6, 'b', linewidth=3,  label="IL-6")
     ax1.plot(t, out_IL8, 'r--',  linewidth=3, label="IL-8")
     ax1.plot(t, out_IL10, 'orange',  linewidth=3, label="IL-10")


     #ax1.legend( ncol = 4, bbox_to_anchor = (0.5,-0.13), loc='upper center', fontsize = 18)
     ax1.legend(bbox_to_anchor = (1,.5), loc='center left', fontsize = 18)
     ax1.set_xlabel('Time (days)', fontsize = 18)
     ax1.set_ylabel('Cytokine concentrations \n (relative values)', fontsize = 18)
     ax1.tick_params(labelsize=18)

     fig.set_figwidth(10) 
     fig.set_figheight(6) 
     fig.tight_layout()
     filename = f'{folder}/{day}_Cytokines.png'
     plt.savefig(filename)

     #Macrophage 
     fig, (ax2) = plt.subplots(1,1)
     ax2.plot(t, out_MR, 'b--',  linewidth=3, label="Resting")
     ax2.plot(t, out_MA, 'black',  linewidth=3, label="Activated")
     #ax2.plot(t, out_A,'r',  linewidth=3, label="A")
     ax2.tick_params(labelsize=18)
     
     fontsize = 18

     #ax2.legend( ncol = 4, bbox_to_anchor = (0.5,-0.13), loc='upper center', fontsize = 18)
     ax2.legend(bbox_to_anchor = (1,.5), loc='center left', fontsize = 18)
     ax2.set_xlabel('Time (days)', fontsize = 18)
     ax2.set_ylabel('Macrophage Concentration \n (cells/mm³ )', fontsize = 18)

     fig.set_figwidth(10) 
     fig.set_figheight(6) 
     fig.tight_layout()
     filename = f'{folder}/{day}_Macrophage.png'
     plt.savefig(filename)

     # S. aureus
     fig, (ax2) = plt.subplots(1,1)
     ax2.plot(t, out_A,'r',  linewidth=3, label="With Immune\n Response")
     #ax2.plot(t, out_A_wo,'b',  linewidth=3, label="Without Immune\n Response")
     ax2.tick_params(labelsize=18)

     #ax2.legend( ncol = 4, bbox_to_anchor = (0.5,-0.13), loc='upper center', fontsize = 18)
     ax2.legend(bbox_to_anchor = (1,.5), loc='center left', fontsize = 18)
     ax2.set_xlabel('Time (days)', fontsize = 18)
     ax2.set_ylabel('S. aureus \n (cells/mm³ )', fontsize = 18)

     fig.set_figwidth(10) 
     fig.set_figheight(6) 
     fig.tight_layout()
     filename = f'{folder}/{day}_S_aureus.png'
     plt.savefig(filename)

     fig, (ax3) = plt.subplots(1,1)
     # Cortisol
     ax3.set_ylabel('Cortisol (ng/day)', fontsize = 18)
     ax3.plot(t, out_COR,'g', linewidth=3, label="Cortisol with glucose influence")
     #ax3.set_title("Cortisol", fontsize = 20)
     ax3.legend( ncol = 4, loc='upper right', fontsize = 18)
     ax3.set_xlabel('Time (days)', fontsize = 18)
     ax3.tick_params(labelsize=18)
     fig.set_figwidth(8) 
     fig.set_figheight(6) 
     fig.tight_layout()
     filename = f'{folder}/{day}_Cortisol.png'
     plt.savefig(filename)

     # TNF
     fig, (ax4) = plt.subplots(1,1)
     ax4.plot(t, out_TNF,'purple', linewidth=3, label="TNF-α with cortisol influence")
     ax4.legend( ncol = 4, loc='lower left', fontsize = 18)
     ax4.set_xlabel('Time (days)', fontsize = 18)
     ax4.tick_params(labelsize=18)

     fig.set_figwidth(8) 
     fig.set_figheight(6) 
     fig.tight_layout()
     filename = f'{folder}/{day}_TNF.png'
     plt.savefig(filename)

# /*******************************************************************************
#  * @param folder - folder directory to be saved
#  * @param filename - name of file to be saved
#  * @param outputs - outputs to be written in the file
#  * @param day - current day
#  ******************************************************************************/
def save_output(folder,filename, outputs, day):
     ### create new file 
     nfilename = f'{folder}/{day}_'+filename
     f = open (nfilename, 'w')
     with open (nfilename, 'a') as f:
          writer = csv.writer(f)
          writer.writerow(outputs)  
     

#if __name__ == "__main__":
     #df = pd.DataFrame() 
     ### INITIAL CONDITIONS FIRST DAY ###
     #ic = [10,5,10,0,0,0.7,0.17,2.24]
     #outputs = W_Cortisol_Cytokines_SAureus(0,df,ic)
     #save_output('wcsa.csv',outputs,0)
     #plots_w_c_sa(t, outputs)