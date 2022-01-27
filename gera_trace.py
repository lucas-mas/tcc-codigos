import fileinput
import numpy as np
import sys

#Forma de utilização:
#python gera_trace.py qtd1 p1 qtd2 p2 qtd3 p3...
#qtd1 é a qtd de probes a serem gerados
#p1 é a probabilidade de sucesso para cada um dos qtd1 traces

#Exemplo1: se eu quero gerar 500 probes com probabilidade de sucesso de 0.1:
## python gera_trace.py 500 0.1

#Exemplo2: se eu quero gerar 500 probes com probabilidade de sucesso 0.1, e 300 probes com probabilidade de sucesso 0.5:
## python gera_trace.py 500 0.1 300 0.5

#essa função recebe dois parâmetros:
#qtd: a quantidade de probes
#p: a probabilidade de sucesso
#e retorna a quantidade de probes desejada
def gera_trace(qtd, p):
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


#extrai a lista de probabilidades
#após esse trecho, a lista vai ficar no formato: [qtd1, p1, qtd2, p2, qtd3, p3].
#por exemplo: [500, 0.5, 500, 0.2, 500, 0.3].
limite=len(sys.argv)-1
lista_de_probabilidades = []
i = 1
while i < limite:
    lista_de_probabilidades.append((int(sys.argv[i]), float(sys.argv[i+1])))
    i = i + 2


#gera a lista de probes (ou seja, o trace). 0 significa um probe perdido, 1 significa um probe entregue
trace = []
for probab in lista_de_probabilidades:
    trace = trace + gera_trace(probab[0], probab[1])
    #print(probab[1], probab[0])

#printa cada probe do trace
for probe in trace:
    print(probe)

