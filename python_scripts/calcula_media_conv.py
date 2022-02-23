import statistics
from pathlib import Path
import math
import sys
import json

import csv


#calcula o intervalo de confiança de 95%
#recebe como parâmetro a quantidade de amostras e o desvio padrão
def calcula_intervalo_confianca(n, dp):
    return 1.96 * (dp / math.sqrt(n))



def escreve_arquivo(lista_de_tempos_de_convergencia, nome_metodo, pi, pf):
    media = statistics.mean(lista_de_tempos_de_convergencia)

    desvio_padrao = statistics.stdev(lista_de_tempos_de_convergencia)
    intervalo_confianca = calcula_intervalo_confianca(len(lista_de_tempos_de_convergencia), desvio_padrao)

        #caso a pessoa tenha passado só um arquivo
    if len(lista_de_tempos_de_convergencia) == 1:
        desvio_padrao = 0
        intervalo_confianca = 0

    else:
        desvio_padrao = statistics.stdev(lista_de_tempos_de_convergencia)
        intervalo_confianca = calcula_intervalo_confianca(len(lista_de_tempos_de_convergencia), desvio_padrao)

    with open("convergencia.csv", "a") as arquivo:
        linha = nome_metodo+','+str(media)+','+str(media-intervalo_confianca)+\
        ','+str(media+intervalo_confianca)+','+str(pi)+','+str(pf)+'\n'
        arquivo.write(linha)