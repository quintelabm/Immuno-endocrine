import src.W_Cortisol_Cytokines_SAureus as wcsa
import src.Glucose_Insulin as gi
import numpy as np
import pandas as pd
import csv
import time

# /*******************************************************************************
#  * @param simulation - F for female and M for male
#  * @param cortisol_exp
#  ******************************************************************************/

def cortisolDecadesOneDay(simulation, parameters, cortisol_exp):
    # Number of days for the simulation (first day is 0)
    days = 1
    print(f'Simulation started! ({days} days)')
    print('Loading files...')
    # create new file 

    if(simulation=='F'):
        folder = 'Output/female/'
        out_filename = 'average_cortisol_female.csv'
    else:
        folder = 'Output/male/'
        out_filename = 'average_cortisol_male.csv'
    print('folder:', folder+out_filename)
    f = open (folder+out_filename, 'w')
    
    # Load experimental data from file
    headers = ['decade', 'value']
    folder_input = 'Input/'
    cortisol_female = pd.read_csv(folder_input+'cortisol_data_female.csv', names=headers)
    cortisol_female_5 = cortisol_female.tail(6)
    cortisol_female_5.reset_index(inplace=True)
    #print(cortisol_female_5)

    cortisol_male = pd.read_csv(folder_input+'cortisol_data_male.csv', names=headers)
    cortisol_male_5 = cortisol_male.tail(6)
    cortisol_male_5.reset_index(inplace=True)
    
    # Simulation time for glucose insulin model (minutes)
    #sim_time_gi = 1440      #24 hours         #Total time of simulation in min 
    sim_time_gi = 720        #12 hours  
    deltaT_gi = pow(10, -3)                   # Step size
    t_gi = np.arange(0,sim_time_gi,deltaT_gi)
    
    # Simulation time for wcsa model (days)
    sim_time_wcsa = 1         # day        # Total time of simulation in min 
    deltaT_wcsa = pow(10, -3)              # Step size
    t_wcsa = np.arange(0,sim_time_wcsa,deltaT_wcsa)
     
    start = time.time()
    #................................
    #   begin simulation time loop
    #................................

    for i in range(0,days,): 
        if (i == 0):
            #|------------------------------------------------------------------|
            #|  run first Cell-Cytokine-Cortisol Model with initial conditions  |
            #|------------------------------------------------------------------|
            print(f'Runing cell-cytokine model day 0...')

            ### create an empty dataframe for first run with initial conditions 
            df = pd.DataFrame() 

            ### call first time of wcsa glucose insulin model outside of time loop
            ### INITIAL CONDITIONS FIRST DAY ###
            ic = [2,0,10,0,0,0.7,0.17,2.32]
            [t_wcsa, outputs_wcsa] = wcsa.W_Cortisol_Cytokines_SAureus(i,df,ic, parameters) 
            ### plot results from the first model 
            ### todo: parameterize with number of saved files we want
            ### as we expect to run for several years
            wcsa.save_output(folder,'bacteria.csv',outputs_wcsa[0],i)
            wcsa.save_output(folder,'ma.csv',outputs_wcsa[1],i)
            wcsa.save_output(folder,'mr.csv',outputs_wcsa[2],i)
            wcsa.save_output(folder,'il10.csv',outputs_wcsa[3],i)
            wcsa.save_output(folder,'TNF.csv',outputs_wcsa[6],i)
            wcsa.save_output(folder,'cortisol.csv',outputs_wcsa[7],i)
            # wcsa.plots_w_c_sa(t_wcsa,folder,outputs_wcsa,i)
            
        ########################################################        
        #### convert cortisol values per day to per minutes ####
        ########################################################

        # Obtain output from cell-cytokine-cortisol model
        cortisol_wcsa = pd.DataFrame(outputs_wcsa[7], columns = ['values'])
        
        # Extract 1000 cortisol values (each 1440 steps)
        print("tamanho cortisol wcsa: ", np.size(cortisol_wcsa))
        
        #cortisol_gi = pd.DataFrame(np.repeat(cortisol_wcsa.values, 1440, axis=0))
        cortisol_gi = pd.DataFrame(np.repeat(cortisol_wcsa.values, 720, axis=0))
        print("tamanho cortisol gi: ", np.size(cortisol_gi))
        cortisol_gi.columns = ['values']
        # Change index to t_gi
        cortisol_gi.set_index(t_gi, inplace=True)
        cortisol_gi.reset_index(inplace=True)
        
        #print('Cortisol results ok')
        #print(mean_cortisol)
        ### write on file cortisol values each day 
        # 8-8h  lembrar que a cada volta soma 1 dia
        #------ forma antiga para testes se preciso
        #mean_cortisol_gi = cortisol_gi.iloc[::480000].mean()
        # mean.append(list(cortisol_gi.iloc[::480000].mean()))
        #mean_cortisol = pd.DataFrame(mean, columns= ['index', 'values'])
        # mean_cortisol.drop('index', axis = 1, inplace=True)
        # mean_cortisol.to_csv('mean_cortisol.csv', index= True)
        #x.append(i)
        
        avg_cor = cortisol_gi.iloc[::480000].mean()['values']
        #avg_cor = cortisol_gi.iloc[::240000].mean()['values']
        data = [i, avg_cor,cortisol_gi['values'].max(), cortisol_gi['values'].min(), cortisol_gi['values'].std()]
        with open (folder+out_filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(data)
            
        #########################################################
        ### run Glucose-Insulin model sending cortisol values ###
        #########################################################
        print(f'Runing glucose model day {i}...')

        [t_gi, outputs_gi] = gi.Glucose_Insulin(1,cortisol_gi)
        gi.save_output(folder,'glucose.csv',outputs_gi[11],i)
        #[t_gi, outputs_gi] = gi.Glucose_Insulin(0,df)
        #gi.plot_GI(t_gi, folder, outputs_gi,i)
        #print('Glicose ok')
        ### convert glucose values per minutes to per day 
        # 1440000 data points
        gluc_intake_gi = pd.DataFrame(outputs_gi[11], columns = ['values']) #Glucose itake
        #print("Tamanho glicose GI: ", np.size(gluc_intake_gi))#720000
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
        #print("Tamanho glicose wcsa: ", np.size(gluc_intake_wcsa))
        gluc_intake_wcsa.set_index(t_wcsa, inplace=True)
        gluc_intake_wcsa.reset_index(inplace=True)
        
        #############################################################################
        ### run Cell-Cytokine-Cortisol Model with glucose output from other model ###
        #############################################################################
        print(f'Runing cell-cytokine model day {i}...')
        ### out_A, out_MA, out_MR, out_IL10, out_IL6, out_IL8, out_TNF, out_COR 
        # ic = [outputs_wcsa[0][999], outputs_wcsa[1][999], outputs_wcsa[2][999], outputs_wcsa[3][999],
        #       outputs_wcsa[4][999], outputs_wcsa[5][999], outputs_wcsa[6][999], outputs_wcsa[7][999]]
        ### run one day for each decade
        if (simulation=='F'):
            cortisol_exp = cortisol_female_5.at[i,'value']
        else:
            cortisol_exp = cortisol_male_5.at[i,'value']
        ic = [2,0,10,0,0,0.7,0.17,cortisol_exp]
        # print(ic)
        [t_wcsa, outputs_wcsa] = wcsa.W_Cortisol_Cytokines_SAureus(i,gluc_intake_wcsa, ic, parameters)
        # write on file
        wcsa.save_output(folder,'bacteria.csv',outputs_wcsa[0],i)
        wcsa.save_output(folder,'ma.csv',outputs_wcsa[1],i)
        wcsa.save_output(folder,'mr.csv',outputs_wcsa[2],i)
        wcsa.save_output(folder,'il10.csv',outputs_wcsa[3],i)
        wcsa.save_output(folder,'TNF.csv',outputs_wcsa[6],i)
        wcsa.save_output(folder,'cortisol.csv',outputs_wcsa[7],i)
        # wcsa.plots_w_c_sa(t_wcsa,folder,outputs_wcsa,i)
        
        # write last simulation to file
        if (i==(days-1)):
            ########################################################        
            #### convert cortisol values per day to per minutes ####
            ########################################################
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
            data = [i+1, avg_cor,cortisol_gi['values'].max(), cortisol_gi['values'].min(), cortisol_gi['values'].std()]
            with open (folder+out_filename, 'a') as f:
                writer = csv.writer(f)
                writer.writerow(data)
        #### end for (time loop) ####
    return [t_wcsa, outputs_wcsa]

        
#-----------------------------------------------------------------------------------------------------------------------
                