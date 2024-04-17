import time
import cortisolDecadesOneDay as cdd              


if __name__ == "__main__":
    start = time.time()
    simulation = 'F'

    #todozao: Fazer o teste mantendo o valor do cortisol fixo e testar da glucose fixa
    # tb pra ver a variação das citocinas com os 7 dias por decada

    #cortisolDecadesOneDay()
    # todo : pegar o valor da primeira decada no arquivo e testar 7 dias uma decada
    # quando funcionar criar o loop e chamar uma vez para cada decada 
    cdd.cortisolDecadesOneDay(simulation=simulation, cortisol_exp=1.65)

    #cortisolDecadesOneWeek(simulation=simulation, cortisol_exp=2.80)
    end = time.time()
    print(f"Time: {int(end - start)}s" )
    
    print('Simulation done. Bye!')
    ### save cortisol graph
    ##post_processing(out_filename)
