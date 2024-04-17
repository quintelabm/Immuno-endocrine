import W_Cortisol_Cytokines_SAureus as wcsa
import Week_Cortisol_Cytokines_SAureus as week_csa
import Glucose_Insulin as gi
import numpy as np
import pandas as pd
import csv
import os 

# /*******************************************************************************
#  * @param simulation - F for female and M for male
#  * @param cortisol_exp
#  ******************************************************************************/

def cortisolDecadesOneWeek(simulation, cortisol_exp):

    # Number of days for the simulation 
    days = 7 #2
    print(f'Simulation started! ({days} days)')
    print('Loading files...')
    # create new file 
    
    if(simulation=='F'):
        folder = f'Output/female_{cortisol_exp}_week'
        out_filename = 'average_cortisol_female.csv'
    else:
        folder = f'Output/male_{cortisol_exp}_week'
        out_filename = 'average_cortisol_male.csv'
    f = open (out_filename, 'w+')
    
    '''     
    ### load experimental data from file
    headers = ['decade', 'value']
    cortisol_female = pd.read_csv('cortisol_data_female.csv', names=headers)
    cortisol_female_5 = cortisol_female.tail(6)
    cortisol_female_5.reset_index(inplace=True)
    #print(cortisol_female_5)
    cortisol_male = pd.read_csv('cortisol_data_male.csv', names=headers)
    cortisol_male_5 = cortisol_male.tail(6)
    cortisol_male_5.reset_index(inplace=True)
    '''

    # Simulation time for glucose insulin model (minutes)
    sim_time_gi = 720      #12 hours  
    deltaT_gi = pow(10, -3)                   # Step size
    t_gi = np.arange(0, sim_time_gi, deltaT_gi)
    
    # Simulation time for wcsa model (days)
    #sim_time_wcsa = 1         # day        # Total time of simulation in min 
    deltaT_wcsa = pow(10, -3)              # Step size
    t_wcsa = np.arange(0, days, deltaT_wcsa)
    print("primeiro tempo", np.size(t_wcsa))
    
    #................................
    #   Begin simulation time loop
    #................................
        
    #for i in range(0,days,): 
        # first day of simulation

    #|------------------------------------------------------------------|
    #|  Run first Cell-Cytokine-Cortisol Model with initial conditions  |
    #|------------------------------------------------------------------|
    print(f'Runing cell-cytokine model day 0...')

    # Create an empty dataframe for first run with initial conditions 
    df = pd.DataFrame()

    # Call first time of wcsa glucose insulin model outside of time loop
    # Initial conditions first day 
    ic = [2,0,10,0,0,0.7,0.17,2.32]
    #[t_wcsa1, outputs_wcsa] = week_csa.Week_Cortisol_Cytokines_SAureus(1,df,ic)
    [t_wcsa1, outputs_wcsa] = wcsa.W_Cortisol_Cytokines_SAureus(0,df,ic)  
    
    # Plot results from the first model 
    wcsa.save_output(folder,'bacteria.csv',outputs_wcsa[0],0)
    wcsa.save_output(folder,'ma.csv',outputs_wcsa[1],0)
    wcsa.save_output(folder,'mr.csv',outputs_wcsa[2],0)
    wcsa.save_output(folder,'il10.csv',outputs_wcsa[3],0)
    wcsa.save_output(folder,'il6.csv',outputs_wcsa[4],0)
    wcsa.save_output(folder,'il8.csv',outputs_wcsa[5],0)
    wcsa.save_output(folder,'TNF.csv',outputs_wcsa[6],0)
    wcsa.save_output(folder,'cortisol.csv',outputs_wcsa[7],0)
    wcsa.plots_w_c_sa(t_wcsa1,folder,outputs_wcsa,0)
    
    #|------------------------------------------------|     
    #| Convert cortisol values per day to per minutes |
    #|------------------------------------------------|

    # Obtain output from cell-cytokine-cortisol model
    cortisol_wcsa = pd.DataFrame(outputs_wcsa[7], columns = ['values'])

    # Extract 1000 cortisol values (each 1440 steps)
    print("tamanho cortisol wcsa: ", np.size(cortisol_wcsa))

    #cortisol_gi = pd.DataFrame(np.repeat(cortisol_wcsa.values, 1440, axis=0))
    cortisol_gi = pd.DataFrame(np.repeat(cortisol_wcsa.values, 720, axis=0))
    #print("tamanho cortisol gi: ", np.size(cortisol_gi))
    cortisol_gi.columns = ['values']
    cortisol_gi.set_index(t_gi, inplace=True)
    cortisol_gi.reset_index(inplace=True)

    avg_cor = cortisol_gi.iloc[::480000].mean()['values']
    #avg_cor = cortisol_gi.iloc[::240000].mean()['values']
    data = [0, avg_cor, cortisol_gi['values'].max(), cortisol_gi['values'].min(), cortisol_gi['values'].std()]
    with open (folder+out_filename, 'a+') as f:
        writer = csv.writer(f)
        writer.writerow(data)
        
    #|-----------------------------------------------------|
    #|  run Glucose-Insulin model sending cortisol values  |
    #|-----------------------------------------------------|
    print(f'Runing glucose model day...')

    [t_gi, outputs_gi] = gi.Glucose_Insulin(1,cortisol_gi)
    #gi.save_output(folder,'glucose.csv',outputs_gi[11],i)
    gi.save_output(folder,'glucose.csv',outputs_gi[11],1)

    gluc_intake_gi = pd.DataFrame(outputs_gi[11], columns = ['values']) #Glucose itake
    
    last_value = gluc_intake_gi['values'].iat[-1]
    temp_gluc_gi = pd.DataFrame(np.repeat(last_value, 720000, axis=0), columns = ['values'])
    #print(temp_gluc_gi.head())
    #print("Tamanho glicose temp: ", np.size(temp_gluc_gi))#840000
    complete_gluc_gi = pd.concat([gluc_intake_gi,temp_gluc_gi])
    # print('ultimo valor? ', gluc_intake_gi[-1])
    #complete_gluc_gi = pd.DataFrame(np.repeat(gluc_intake_gi.values, 2, axis=0))
    #print("Tamanho glicose completo: ", np.size(complete_gluc_gi))#840000
    ### Obtain cortisol 1440000 points
    #gluc_intake_wcsa = gluc_intake_gi.iloc[::1440]

    gluc_intake_wcsa = complete_gluc_gi.iloc[::1440]
    print(" O Tamanho glicose wcsa: ", np.size(gluc_intake_wcsa)) #1000
 
    gluc_intake_wcsa = pd.concat([gluc_intake_wcsa,gluc_intake_wcsa,gluc_intake_wcsa,gluc_intake_wcsa,gluc_intake_wcsa,gluc_intake_wcsa,gluc_intake_wcsa], axis =0) # 7 days = 70000
    print("O tamanho da glicose para 1 semana é:", np.size(gluc_intake_wcsa))
    print("gluc = \n:", gluc_intake_wcsa)

    #gluc_intake_wcsa['indices'] = t_wcsa
    
    #gluc_intake_wcsa.reset_index(drop = True, inplace=True) # 0 até 699
    gluc_intake_wcsa.set_index(t_wcsa, inplace=True)
    gluc_intake_wcsa.reset_index(inplace=True)

   #gluc_intake_wcsa.columns = ['index','values' inplace = True]
    #gluc_intake_wcsa.rename(columns = {'':'index'}, inplace =True)
    ##gluc_intake_wcsa.index.name = 'index'
    print("Tamanho t_wcsa", np.size(t_wcsa))
    #print("O tamanho da glicose para 1 semana é:", np.size(gluc_intake_wcsa))
    print("gluc = \n:", gluc_intake_wcsa)

    #print("index: ",  gluc_intake_wcsa.indices.to_string(index=False))
 
    #print(gluc_intake_wcsa)
    ### indice = gluc_intake_wcsa['index'].sub(t_wcsa).abs().idxmin()
    #indice = gluc_intake_wcsa.index.sub(t_wcsa).abs().idxmin()
    #tempo = t_wcsa*7
    #print("tempo wcsa:", np.size(t_wcsa))
    #print("tempo:", np.size(tempo))
    #print("esse é o indice: ", indice)
    
    #|--------------------------------------------------------------------------|
    #| run Cell-Cytokine-Cortisol Model with glucose output from other model    |
    #|--------------------------------------------------------------------------|
    print(f'Runing cell-cytokine model day...')
    ### out_A, out_MA, out_MR, out_IL10, out_IL6, out_IL8, out_TNF, out_COR 
    # ic = [outputs_wcsa[0][999], outputs_wcsa[1][999], outputs_wcsa[2][999], outputs_wcsa[3][999],
    #       outputs_wcsa[4][999], outputs_wcsa[5][999], outputs_wcsa[6][999], outputs_wcsa[7][999]]
    ### run one day for each decade
    #if (simulation=='F'):
    #    cortisol_exp = cortisol_female_5.at[i,'value']
    #else:
    #    cortisol_exp = cortisol_male_5.at[i,'value']
    ic = [2,0,10,0,0,0.7,0.17,cortisol_exp]
    # print(ic)
    #days=1
    [t_wcsa, outputs_wcsa] = week_csa.Week_Cortisol_Cytokines_SAureus(days,gluc_intake_wcsa, ic)

    # write on file
    week_csa.save_output(folder,'bacteria.csv',outputs_wcsa[0],days)
    week_csa.save_output(folder,'ma.csv',outputs_wcsa[1],days)
    week_csa.save_output(folder,'mr.csv',outputs_wcsa[2],days)
    week_csa.save_output(folder,'il10.csv',outputs_wcsa[3],days)
    wcsa.save_output(folder,'il6.csv',outputs_wcsa[4],days)
    wcsa.save_output(folder,'il8.csv',outputs_wcsa[5],days)
    week_csa.save_output(folder,'TNF.csv',outputs_wcsa[6],days)
    week_csa.save_output(folder,'cortisol.csv',outputs_wcsa[7],days)
    week_csa.plots_w_c_sa(t_wcsa,folder,outputs_wcsa,days)
    
    # write last simulation to file
    '''
    if (i==(days-1)):
        #|-----------------------------------------------------|       
        #|  convert cortisol values per day to per minutes     |
        #|-----------------------------------------------------|
        # Obtain output from cell-cytokine-cortisol model
        cortisol_wcsa = pd.DataFrame(outputs_wcsa[7], columns = ['values'])
        # Extract 1000 cortisol values (each 1440 steps)
        #cortisol_gi = pd.DataFrame(np.repeat(cortisol_wcsa.values, 1440, axis=0))
        cortisol_gi = pd.DataFrame(np.repeat(cortisol_wcsa.values, 720, axis=0))
        cortisol_gi.columns = ['values']
        # Change index to t_gi
        cortisol_gi.set_index(t_gi, inplace=True)
        cortisol_gi.reset_index(inplace=True)
        
        avg_cor = cortisol_gi.iloc[::480000].mean()['values']
        #avg_cor = cortisol_gi.iloc[::240000].mean()['values']
        print("tamanho da media do COR: ", np.size(avg_cor))
        data = [i+1, avg_cor,cortisol_gi['values'].max(), cortisol_gi['values'].min(), cortisol_gi['values'].std()]
        with open (out_filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(data)
    '''
    #### end for (time loop) ####
        