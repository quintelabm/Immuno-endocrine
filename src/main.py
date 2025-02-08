import time
import cortisolDecadesOneDay as cdd              


ktc= 3.43
kmtc= 2.78
kmct= 8.69
kcd= 1.55
klt= 3.35
klt6= 1.20
Cmax= 3
n_610= 34.8
n_66= 560
n_6TNF= 185
n_M10= 4.35 #da erro pra rodar a SA
n_MTNF= 0.1
h_610= 4
h_66= 1
h_6TNF= 2
h_MTNF= 3.16
k_6= 4.64
k_6m= 0.01
k_6TNF= 0.81
k_MTNF= 8.65 #da erro pra rodar a SA
q_IL6= 0.6 #da erro pra rodar a SA
beta_A= 0.02 #da erro pra rodar a SA
k_A=50 #da erro pra rodar a SA
m_A= 0.9 #da erro pra rodar a SA
k_m= 1.414 #da erro pra rodar a SA

if __name__ == "__main__":
    start = time.time()
    simulation = 'F'

    #todozao: Fazer o teste mantendo o valor do cortisol fixo e testar da glucose fixa
    # tb pra ver a variação das citocinas com os 7 dias por decada

    #cortisolDecadesOneDay()
    # todo : pegar o valor da primeira decada no arquivo e testar 7 dias uma decada
    # quando funcionar criar o loop e chamar uma vez para cada decada 

    cortisol_parameters = [ktc, kmtc, kmct, klt6]
    brady_parameters = [n_610, n_66, n_6TNF, n_MTNF, h_610, h_66, h_6TNF, h_MTNF, k_6, k_6m, k_6TNF]
    quintela_parameters = []
    
    cdd.cortisolDecadesOneDay(simulation, cortisol_parameters, brady_parameters, quintela_parameters, cortisol_exp=2.32)

    #cortisolDecadesOneWeek(simulation=simulation, cortisol_exp=2.80)
    end = time.time()
    print(f"Time: {int(end - start)}s" )
    
    print('Simulation done. Bye!')
    ### save cortisol graph
    ##post_processing(out_filename)
