
import src.cortisolDecadesOneDay as cdd
import time
import uncertainpy as un
import chaospy as cp


def citokynes(ktc,kmtc):
  parameters = [ktc,kmtc]
  simulation = 'F'
  output = cdd.cortisolDecadesOneDay(simulation, parameters,
                                 cortisol_exp=2.32)
  [t_wcsa, outputs_wcsa] = output
  [out_A, out_MA, out_MR, out_IL10, out_IL6, out_IL8, out_TNF, out_COR] = outputs_wcsa
  return t_wcsa, out_IL6



if __name__ == "__main__":
    start = time.time()

     # Create the distributions
    ktc  = cp.Uniform(2.43, 4.43)         # ng/(pg·h)                                             # The magnitude of cortisol activation by TNF
    kmtc = cp.Uniform(1.78, 3.78)  

    # Create a model from the function and add labels
    model = un.Model(citokynes, labels=["Time (s)", "IL6 (pg/mL)"])

    # Define the parameters dictionary
    parameters = {
        "ktc": ktc,
        "kmtc": kmtc
    }

    # We can use the parameters dictionary directly
    # when we set up the uncertainty quantification
    UQ = un.UncertaintyQuantification(model=model, parameters=parameters)

    # Perform the uncertainty quantification,
    # which automatically use the Rosenblatt transformation
    # We set the seed to easier be able to reproduce the result
    data = UQ.quantify(seed=10)
    
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
