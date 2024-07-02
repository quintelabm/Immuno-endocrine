from pydoc import locate
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def week_post_processing(simulation):

    #--- Generate Cortisol Plot by paper ---
    decades = ['30-40', '40-50', '50-60', '60-70', '70-80', '80-90']
    headers = ['index', 'avg','max','min','std']
    x = [30, 35, 45, 55, 65, 75, 85]
    if(simulation=='F'):
        cortisol_exp = [2.32, 2.24, 2.25, 2.43, 2.55, 2.80]
    else:
        cortisol_exp = [2.32, 2.25, 2.55, 2.62, 2.84, 3.13]

    #IL6
    fig, (ax2) = plt.subplots(1,1)  
    for i in range(0,6):
        if(simulation=='F'):
            fname = f'Output/female_{cortisol_exp[i]}_week/7_il6.csv'
        else:
            fname = f'Output/male_{cortisol_exp[i]}_week/7_il6.csv'
        valor = pd.read_csv(fname, header=None)
        y = valor.T
        d = decades[i]
        label = f'Década {d}'
        x = np.linspace(0,7,7000)
        out_IL6 = y[0]
        #out_TNF = 100 * (out_TNF - min(out_TNF)) / (max(out_TNF) - min(out_TNF))
        ax2.plot(x,out_IL6,'.',label=label)
       
        
    ax2.legend(bbox_to_anchor = (0.5, -0.15), loc='upper center', fontsize = 18, fancybox=True, shadow=True, ncol=5)    
    ax2.set_ylabel('IL-6 concentrations \n (relative values)', fontsize = 18)
    ax2.set_xlabel('Time (days)', fontsize = 18)
    #ax1.figure(figsize=(10, 10))
    fig.set_figwidth(15) 
    fig.set_figheight(6) 
    fig.tight_layout()
    plt.savefig(f'Output/week_post_processing/IL6_{simulation}.png', bbox_inches='tight') #defines file name based on simulation value

    #IL8
    fig, (ax2) = plt.subplots(1,1)  
    for i in range(0,6):
        if(simulation=='F'):
            fname = f'Output/female_{cortisol_exp[i]}_week/7_il8.csv'
        else:
            fname = f'Output/male_{cortisol_exp[i]}_week/7_il8.csv'
        valor = pd.read_csv(fname, header=None)
        y = valor.T
        d = decades[i]
        label = f'Década {d}'
        x = np.linspace(0,7,7000)
        out_IL8 = y[0]
        #out_TNF = 100 * (out_TNF - min(out_TNF)) / (max(out_TNF) - min(out_TNF))
        ax2.plot(x,out_IL8,'.',label=label)
       
        
    ax2.legend(bbox_to_anchor = (0.5, -0.15), loc='upper center', fontsize = 18, fancybox=True, shadow=True, ncol=5)    
    ax2.set_ylabel('IL-8 concentrations \n (relative values)', fontsize = 18)
    ax2.set_xlabel('Time (days)', fontsize = 18)
    #ax1.figure(figsize=(10, 10))
    fig.set_figwidth(15) 
    fig.set_figheight(6) 
    fig.tight_layout()
    plt.savefig(f'Output/week_post_processing/IL8_{simulation}.png', bbox_inches='tight')



    #IL10
    fig, (ax2) = plt.subplots(1,1)  
    for i in range(0,6):
        if(simulation=='F'):
            fname = f'Output/female_{cortisol_exp[i]}_week/7_il10.csv'
        else:
            fname = f'Output/male_{cortisol_exp[i]}_week/7_il10.csv'
        valor = pd.read_csv(fname, header=None)
        y = valor.T
        d = decades[i]
        label = f'Década {d}'
        x = np.linspace(0,7,7000)
        out_IL10 = y[0]
        #out_TNF = 100 * (out_TNF - min(out_TNF)) / (max(out_TNF) - min(out_TNF))
        ax2.plot(x,out_IL10,'.',label=label)
       
        
    ax2.legend(bbox_to_anchor = (0.5, -0.15), loc='upper center', fontsize = 18, fancybox=True, shadow=True, ncol=5)    
    ax2.set_ylabel('IL-10 concentrations \n (relative values)', fontsize = 18)
    ax2.set_xlabel('Time (days)', fontsize = 18)
    #ax1.figure(figsize=(10, 10))
    fig.set_figwidth(15) 
    fig.set_figheight(6) 
    fig.tight_layout()
    #plt.savefig('Output/week_post_processing/IL10_female.png', bbox_inches='tight')   #for F simulations
    plt.savefig(f'Output/week_post_processing/IL10_{simulation}.png', bbox_inches='tight')    #for M simulations



    #TNF
    fig, (ax2) = plt.subplots(1,1)  
    for i in range(0,6):
        if(simulation=='F'):
            fname = f'Output/female_{cortisol_exp[i]}_week/7_TNF.csv'
        else:
            fname = f'Output/male_{cortisol_exp[i]}_week/7_TNF.csv'
        valor = pd.read_csv(fname, header=None)
        y = valor.T
        d = decades[i]
        label = f'Década {d}'
        x = np.linspace(0,7,7000)
        out_TNF = y[0]
        #out_TNF = 100 * (out_TNF - min(out_TNF)) / (max(out_TNF) - min(out_TNF))
        ax2.plot(x,out_TNF,'.',label=label)
       
        
    ax2.legend(bbox_to_anchor = (0.5, -0.15), loc='upper center', fontsize = 18, fancybox=True, shadow=True, ncol=5)    
    ax2.set_ylabel('TNF concentrations \n (relative values)', fontsize = 18)
    ax2.set_xlabel('Time (days)', fontsize = 18)
    #ax1.figure(figsize=(10, 10))
    fig.set_figwidth(15) 
    fig.set_figheight(6) 
    fig.tight_layout()
    plt.savefig(f'Output/week_post_processing/TNF_{simulation}.png', bbox_inches='tight')    #for M simulations



    #Cortisol
    fig, (ax2) = plt.subplots(1,1)  
    for i in range(0,6):
        if(simulation=='F'):
            fname = f'Output/female_{cortisol_exp[i]}_week/7_cortisol.csv'
        else:
            fname = f'Output/male_{cortisol_exp[i]}_week/7_cortisol.csv'    #for M simulations
        valor = pd.read_csv(fname, header=None)
        y = valor.T
        d = decades[i]
        label = f'Década {d}'
        x = np.linspace(0,7,7000)
        out_cortisol = y[0]
        #out_TNF = 100 * (out_TNF - min(out_TNF)) / (max(out_TNF) - min(out_TNF))
        ax2.plot(x,out_cortisol,'.',label=label)
       
        
    ax2.legend(bbox_to_anchor = (0.5, -0.15), loc='upper center', fontsize = 18, fancybox=True, shadow=True, ncol=5)    
    ax2.set_ylabel('Cortisol concentrations \n (relative values)', fontsize = 18)
    ax2.set_xlabel('Time (days)', fontsize = 18)
    #ax1.figure(figsize=(10, 10))
    fig.set_figwidth(15) 
    fig.set_figheight(6) 
    fig.tight_layout()
    plt.savefig(f'Output/week_post_processing/Cortisol_{simulation}.png', bbox_inches='tight')   #for F simulations



    #Macrophage
    fig, (ax2) = plt.subplots(1,1)  
    for i in range(0,6):
        if(simulation=='F'):
            fname = f'Output/female_{cortisol_exp[i]}_week/7_ma.csv'
        else:
            fname = f'Output/male_{cortisol_exp[i]}_week/7_ma.csv'
        valor = pd.read_csv(fname, header=None)
        y = valor.T
        d = decades[i]
        label = f'Década {d}'
        x = np.linspace(0,7,7000)
        out_ma = y[0]
        #out_TNF = 100 * (out_TNF - min(out_TNF)) / (max(out_TNF) - min(out_TNF))
        ax2.plot(x,out_ma,'.',label=label)
       
        
    ax2.legend(bbox_to_anchor = (0.5, -0.15), loc='upper center', fontsize = 18, fancybox=True, shadow=True, ncol=5)    
    ax2.set_ylabel('Macrophage concentrations \n (relative values)', fontsize = 18)
    ax2.set_xlabel('Time (days)', fontsize = 18)
    #ax1.figure(figsize=(10, 10))
    fig.set_figwidth(15) 
    fig.set_figheight(6) 
    fig.tight_layout()
    #plt.savefig('Output/week_post_processing/MA_female.png', bbox_inches='tight')   #for F simulations
    plt.savefig(f'Output/week_post_processing/MA_{simulation}.png', bbox_inches='tight')    #for M simulations

    print('Post-processing done. Bye!')


''' 
    # Cortisol
    fig, (ax1) = plt.subplots(1,1)  
    for i in range(1,6):
        fname = f'Output/cortisol/{i}_cortisol.csv'
        valor = pd.read_csv(fname, header=None)
        y = valor.T
        d = decades[i]
        label = f'Década {d}'
        x = np.linspace(0,7,7000)
        ax1.plot(x,y[0],'.',label=label)
        
    ax1.legend(bbox_to_anchor = (0.5, -0.15), loc='upper center', fontsize = 18, fancybox=True, shadow=True, ncol=5)    
    ax1.set_ylabel('Cortisol (ng/day)', fontsize = 18)
    ax1.set_xlabel('Time (days)', fontsize = 18)
    #ax1.figure(figsize=(10, 10))
    fig.set_figwidth(15) 
    fig.set_figheight(6) 
    fig.tight_layout()
    plt.savefig('Output/cortisol/cortisol.png', bbox_inches='tight')     


    # TNF
    fig, (ax2) = plt.subplots(1,1)  
    for i in range(1,6):
        fname = f'Output/tnf/{i}_TNF.csv'
        valor = pd.read_csv(fname, header=None)
        y = valor.T
        d = decades[i]
        label = f'Década {d}'
        x = np.linspace(0,7,7000)
        out_TNF = y[0]
        #out_TNF = 100 * (out_TNF - min(out_TNF)) / (max(out_TNF) - min(out_TNF))
        ax2.plot(x,out_TNF,'.',label=label)
       
        
    ax2.legend(bbox_to_anchor = (0.5, -0.15), loc='upper center', fontsize = 18, fancybox=True, shadow=True, ncol=5)    
    ax2.set_ylabel('TNF-α concentrations \n (relative values)', fontsize = 18)
    ax2.set_xlabel('Time (days)', fontsize = 18)
    #ax1.figure(figsize=(10, 10))
    fig.set_figwidth(15) 
    fig.set_figheight(6) 
    fig.tight_layout()
    plt.savefig('Output/tnf/tnf.png', bbox_inches='tight')
''' 
   
''' 
    # S.aureus
    fig, (ax3) = plt.subplots(1,1)  
    for i in range(1,6):
        fname = f'Output/bacteria/{i}_bacteria.csv'
        valor = pd.read_csv(fname, header=None)
        y = valor.T
        d = decades[i]
        label = f'Década {d}'
        x = np.linspace(0,7,7000)
        ax3.plot(x,y[0],'.',label=label)
        
    ax3.legend(bbox_to_anchor = (0.5, -0.15), loc='upper center', fontsize = 18, fancybox=True, shadow=True, ncol=5)    
    ax3.set_ylabel('S. aureus \n (cells/mm³)' , fontsize = 18)
    ax3.set_xlabel('Time (days)', fontsize = 18)
    fig.set_figwidth(15) 
    fig.set_figheight(6) 
    fig.tight_layout()
    plt.savefig('Output/bacteria/bacteria.png', bbox_inches='tight') 

    # Citocinas
    fig, (ax4) = plt.subplots(1,1)

    #for i in range(1,6):
    fname_il6  = f'Output/il6/6_il6.csv'
    fname_il8  = f'Output/il8/6_il8.csv'
    fname_il10 = f'Output/il10/6_il10.csv'
    valor_il6 = pd.read_csv(fname_il6, header=None)
    valor_il8 = pd.read_csv(fname_il8, header=None)
    valor_il10 = pd.read_csv(fname_il10, header=None)
    y_il6 = valor_il6.T
    y_il8 = valor_il8.T
    y_il10 = valor_il10.T
    d = decades[5]
    label_il6 =  f'IL-6  Década {d}'
    label_il8 =  f'IL-8  Década {d}'
    label_il10 = f'IL-10 Década {d}'
    x = np.linspace(0,7,7000)
    ax4.plot(x,y_il6[0],'.',label=label_il6)
    ax4.plot(x,y_il8[0],'.',label=label_il8)
    ax4.plot(x,y_il10[0],'.',label=label_il10)
        
    ax4.legend(bbox_to_anchor = (0.5, -0.15), loc='upper center', fontsize = 18, fancybox=True, shadow=True, ncol=5)    
    ax4.set_ylabel('Cytokine concentrations \n (relative values)', fontsize = 18)
    ax4.set_xlabel('Time (days)', fontsize = 18)
    fig.set_figwidth(15) 
    fig.set_figheight(6) 
    fig.tight_layout()
    plt.savefig('Output/citocinas/citocina.png', bbox_inches='tight')
''' 
   
    



'''
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
     filename = f'{day}_Cytokines.png'
     plt.savefig(filename)

'''



'''
    for i in range(1,6):
        fname = f'Output/cortisol/1_cortisol.csv'
        valor = pd.read_csv(fname, header=None)
        y = valor.T
        d = decades[i]
        label = 'Cortisol without \nglucose influence'
        x = np.linspace(0,1,7000)
        plt.plot(x,y[0],'-',lw=3,label=label)
        plt.legend(loc='upper right',fontsize=16)
        
        plt.ylabel('Cortisol (ng/day)', fontsize = 18)
        plt.xlabel('Time (days)', fontsize = 18)
        plt.savefig('Output/cortisol/cortisol_without.png',bbox_inches='tight') 

'''

def post_processing(days):
    #--- Generate Cortisol Plot by paper ---
    decades = ['30-40', '40-50', '50-60', '60-70', '70-80', '80-90']

    # TNF
    fig, (ax2) = plt.subplots(1,1)  
    # todo: repeticao para pegar de cada pasta (valores de cortisol j)
    #cortisol_exp = [2.32, 2.24, 2.25, 2.43, 2.55, 2.80]
    cortisol_exp = [2.32, 2.24, 2.25, 2.43, 2.55, 2.80]
    for j in range(0,6):
        # todo: parametrizar para numero de dias simulado
        for i in range(1,days):
            fname = f'Output/female_{cortisol_exp[j]}_week/{i}_TNF.csv'
            valor = pd.read_csv(fname, header=None)
            y = valor.T
            d = decades[j]
            label = f'Década {d}'
            x = np.linspace(0,days,1000)
            out_TNF = y[0]
            #out_TNF = 100 * (out_TNF - min(out_TNF)) / (max(out_TNF) - min(out_TNF))
            ax2.plot(x,out_TNF,'.',label=label)

    ax2.legend(bbox_to_anchor = (0.5, -0.15), loc='upper center', fontsize = 18, fancybox=True, shadow=True, ncol=5)    
    ax2.set_ylabel('TNF-α concentrations \n (relative values)', fontsize = 18)
    ax2.set_xlabel('Time (days)', fontsize = 18)
    #ax1.figure(figsize=(10, 10))
    fig.set_figwidth(15) 
    fig.set_figheight(6) 
    fig.tight_layout()
    plt.savefig('Output/tnf.png', bbox_inches='tight')


if __name__ == "__main__":
    week_post_processing()
    #post_processing(2)