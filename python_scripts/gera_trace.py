import fileinput
import numpy as np
import sys
import os


pasta_traces='../traces'


#essa função recebe dois parâmetros:
#qtd: a quantidade de probes
#p: a probabilidade de sucesso
#e retorna a quantidade de probes desejada
def gera_trace_parcial(qtd, p):
    lista = []
    for i in range(qtd):
        #o parâmetro 1 significa que vai fazer o experimento uma vez só. cada iteracao gera 0 ou 1, com probabilidade de sucesso p.
        lista.append((np.random.binomial(1, p)))
    return lista

#(essa funcao nao esta em uso)
#gera o histórico de probabilidades.
#por exemplo, se foram 500 probes com probabilidade de sucesso 0,5,
#retorna 500 vezes o 0,5.
def gera_historico(p, qtd):
    historico = np.full(qtd, p)
    return historico


def gera_trace_completo(lista_de_probabilidades):
    #gera a lista de probes (ou seja, o trace). 0 significa um probe perdido, 1 significa um probe entregue
    trace = []
    for probab in lista_de_probabilidades:
        trace = trace + gera_trace_parcial(probab[0], probab[1])
    return trace

def gera_todos_traces(lista_de_probabilidades, qtd_traces):
    nome_pasta=lista_de_probabilidades.replace(' ', '-')+'-'+str(qtd_traces)
    lista = lista_de_probabilidades.split(" ")

    lista_tuplas=[]
    for i in range(0, len(lista)-1, 2):
        tupla = (int(lista[i]), float(lista[i+1]))
        lista_tuplas.append(tupla)
    

    pasta_final=pasta_traces+'/'+nome_pasta
    if not os.path.isdir(pasta_final):
        os.makedirs(pasta_final)

    for i in range(1, qtd_traces+1):
        nome_arquivo=pasta_final+'/'+str(i)
        trace_completo = gera_trace_completo(lista_tuplas)
        trace_completo = [str(x) for x in trace_completo]
        with open(nome_arquivo, "w") as arquivo:
            arquivo.write('\n'.join(trace_completo))

    return pasta_final

