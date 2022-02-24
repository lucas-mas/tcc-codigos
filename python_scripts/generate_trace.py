import numpy as np
import os


traces_folder='../traces'


#essa função recebe dois parâmetros:
#qtd: a quantidade de probes
#p: a probabilidade de sucesso
#e retorna a quantidade de probes desejada
def generate_partial_trace(qtd, p):
    list = []
    for i in range(qtd):
        #o parâmetro 1 significa que vai fazer o experimento uma vez só. cada iteracao gera 0 ou 1, com probabilidade de sucesso p.
        list.append((np.random.binomial(1, p)))
    return list

#(essa funcao nao esta em uso)
#gera o histórico de probabilidades.
#por exemplo, se foram 500 probes com probabilidade de sucesso 0,5,
#retorna 500 vezes o 0,5.
def generate_real_probability_history(p, qtd):
    historico = np.full(qtd, p)
    return historico


def generate_full_trace(probability_list):
    #gera a list de probes (ou seja, o trace). 0 significa um probe perdido, 1 significa um probe entregue
    trace = []
    for probab in probability_list:
        trace = trace + generate_partial_trace(probab[0], probab[1])
    return trace

def generate_all_traces(probability_list, number_of_traces):
    folder_name=probability_list.replace(' ', '-')+'-'+str(number_of_traces)
    list = probability_list.split(" ")

    list_tuple_qtty_probability=[]
    for i in range(0, len(list)-1, 2):
        tuple_qtty_probability = (int(list[i]), float(list[i+1]))
        list_tuple_qtty_probability.append(tuple_qtty_probability)
    

    final_traces_folder=traces_folder+'/'+folder_name
    if not os.path.isdir(final_traces_folder):
        os.makedirs(final_traces_folder)

    for i in range(1, number_of_traces+1):
        file_name=final_traces_folder+'/'+str(i)
        full_trace = generate_full_trace(list_tuple_qtty_probability)
        full_trace = [str(x) for x in full_trace]
        with open(file_name, "w") as file:
            file.write('\n'.join(full_trace))

    return final_traces_folder

