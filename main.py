import W_Cortisol_Cytokines_SAureus as wcsa
import Glucose_Insulin as gi
import numpy as np
import pandas as pd

if __name__ == "__main__":
    # Simulation tim for glucose insulin model
    sim_time_gi = 1440 #24 hours         #Total time of simulation in min 
    deltaT_gi = pow(10, -3) # -          # Step size
    t_gi = np.arange(0,sim_time_gi,deltaT_gi)
    print(np.size(t_gi))
    
    #simulation time for wcsa model
    #sim_time = 1         # day        # Total time of simulation in min 
    #deltaT = pow(10, -4) # -          # Step size
    #t = np.arange(0,sim_time,deltaT)
     
    # todo loop
    [t, outputs_wcsa] = wcsa.W_Cortisol_Cytokines_SAureus()
    #wcsa.plots_w_c_sa(t,outputs_wcsa)
    # obtain cortisol 10000 points
    cortisol = pd.DataFrame(outputs_wcsa[7])
    #print(cortisol)
    # generate with 1440000
    cortisol_gi = pd.DataFrame(np.repeat(cortisol.values, 144, axis=0))
    cortisol_gi.columns = ['values'] 
    #print(cortisol_gi)
    # todo: funcao para converter de por dia para por minutos

    outputs_gi = gi.Glucose_Insulin(cortisol_gi)
    #gi.plot_GI(outputs_gi)
    # converter de por minutos para por dia
    