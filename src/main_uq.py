
import cortisolDecadesOneDay as cdd
import time
import uncertainpy as un
import chaospy as cp


def COR(ktc,kmtc, kmct, kcd, klt, klt6, cmax, nM10, nTNF10, nMTNF, hM10, hTNF10, hMTNF, k_6, k_6m, k_8, k_8m, k_10, k_10m, k_TNF, k_TNFM, k_MTNF, q_IL6, q_IL8, q_TNF, m_A, MR_max, k_MA, k_MR):
  simulation = 'F'

  cortisol_parameters = [ktc, kmtc, kmct, kcd, klt, klt6, cmax]
  brady_parameters = [nM10, nTNF10, nMTNF, hM10, hTNF10, hMTNF, k_6, k_6m, k_8, k_8m, k_10, k_10m, k_TNF, k_TNFM, k_MTNF, q_IL6, q_IL8, q_TNF]
  quintela_parameters = [m_A, MR_max, k_MA, k_MR]
  
  output = cdd.cortisolDecadesOneDay(simulation, cortisol_parameters, brady_parameters, 
                                      quintela_parameters, cortisol_exp=2.32)
  [t_wcsa, outputs_wcsa] = output
  [out_A, out_MA, out_MR, out_IL10, out_IL6, out_IL8, out_TNF, out_COR] = outputs_wcsa
  return t_wcsa, out_COR



if __name__ == "__main__":
    start = time.time()

     # Create the distributions
    ktc  = cp.Uniform(3.43*0.9, 3.43*1.1)         # ng/(pg·h)                                             # The magnitude of cortisol activation by TNF
    kmtc = cp.Uniform(2.78*0.9, 2.78*1.1) 
    kmct = cp.Uniform(8.69*0.9, 8.69*1.1) 
    kcd = cp.Uniform(1.55*0.9, 1.55*1.1)
    klt = cp.Uniform(3.35*0.9, 3.35*1.1)
    klt6 = cp.Uniform(1.35*0.9, 1.35*1.1)
    cmax = cp.Uniform(3*0.9, 3*1.1)

    nM10 = cp.Uniform(4.35*0.9, 4.35*1.1)
    nTNF10 = cp.Uniform(17.4*0.9, 17.4*1.1)
    nMTNF = cp.Uniform(0.1*0.9, 0.1*1.1)
    hM10 = cp.Uniform(0.3*0.9, 0.3*1.1)
    hTNF10 = cp.Uniform(3*0.9, 3*1.1)
    hMTNF = cp.Uniform(3.16*0.9, 3.16*1.1)

    k_6 = cp.Uniform(4.64*0.9, 4.64*1.1)
    k_6m = cp.Uniform(0.01*0.9, 0.01*1.1)
    k_8 = cp.Uniform(0.464*0.9, 0.464*1.1)
    k_8m = cp.Uniform(0.056*0.9, 0.056*1.1)
    k_10 = cp.Uniform(1.1*0.9, 1.1*1.1)
    k_10m = cp.Uniform(0.19*0.9, 0.19*1.1)
    k_TNF = cp.Uniform(200*0.9, 200*1.1)
    k_TNFM = cp.Uniform(1.5*0.9, 1.5*1.1)
    k_MTNF = cp.Uniform(8.65*0.9, 8.65*1.1)

    q_IL6 = cp.Uniform(0.6*0.9, 0.6*1.1)
    q_IL8 = cp.Uniform(0.2*0.9, 0.2*1.1)
    q_TNF = cp.Uniform(0.14*0.9, 0.14*1.1)

    m_A = cp.Uniform(0.9*0.9, 0.9*1.1)
    MR_max = cp.Uniform(5*0.9, 5*1.1)
    k_MA = cp.Uniform(2.51*0.9, 2.51*1.1)
    k_MR = cp.Uniform(6*0.9, 6*1.1)

    # Create a model from the function and add labels
    model = un.Model(COR, labels=["Time (day)", "Cortisol (pg/mL)"])

    # Define the parameters dictionary
    parameters = {
        "ktc": ktc,
        "kmtc": kmtc,
        "kmct": kmct,
        "kcd": kcd,
        "klt": klt,
        "klt6": klt6,
        "cmax": cmax,
        "nM10": nM10,
        "nTNF10": nTNF10,
        "nMTNF": nMTNF,
        "hM10": hM10,
        "hTNF10": hTNF10,
        "hMTNF": hMTNF,
        "k_6": k_6,
        "k_6m": k_6m,
        "k_8": k_8,
        "k_8m": k_8m,
        "k_10": k_10,
        "k_10m": k_10m,
        "k_TNF": k_TNF,
        "k_TNFM": k_TNFM,
        "k_MTNF": k_MTNF,
        "q_IL6": q_IL6,
        "q_IL8": q_IL8,
        "q_TNF": q_TNF,
        "m_A": m_A,
        "MR_max": MR_max,
        "k_MA": k_MA,
        "k_MR": k_MR
    }

    # We can use the parameters dictionary directly
    # when we set up the uncertainty quantification
    UQ = un.UncertaintyQuantification(model=model, parameters=parameters)

    # Perform the uncertainty quantification,
    # which automatically use the Rosenblatt transformation
    # We set the seed to easier be able to reproduce the result
    data = UQ.quantify(seed=42, plot="condensed_no_sensitivity", nr_mc_samples=100, method="mc")#polynomial_order=3
    
    end = time.time()
    print(f"Time: {int(end - start)}s" )
    
    print('Simulation done. Bye!')
    ### save cortisol graph
    ##post_processing(out_filename)

        


        


# if __name__ == "__main__":
#     start = time.time()
#     simulation = 'F'

#     #todozao: Fazer o teste mantendo o valor do cortisol fixo e testar da glucose fixa
#     # tb pra ver a variação das citocinas com os 7 dias por decada

#     ktc  = 3.43       # ng/(pg·h)                                             # The magnitude of cortisol activation by TNF
#     kmtc = 2.78

#     #cdd.cortisolDecadesOneDay()
#     # todo : pegar o valor da primeira decada no arquivo e testar 7 dias uma decada
#     # quando funcionar criar o loop e chamar uma vez para cada decada 
#     cdd.cortisolDecadesOneDay(simulation=simulation, parameters=[ktc, kmtc], cortisol_exp=2.32)

#     #cdw.cortisolDecadesOneWeek(simulation=simulation, cortisol_exp=2.80)
#     end = time.time()
#     print(f"Time: {int(end - start)}s" )
    
#     print('Simulation done. Bye!')
#     ### save cortisol graph
#     ##post_processing(out_filename)
