import fileinput
import numpy as np
import sys
from exporta_metodo_e_parametros import *
from gera_trace import *

import subprocess


qtd_probes=200000
qtd_traces = 3

metodo_e_parametros=nome_metodo+" "+' '.join(parametros)


parametros_trace=str(qtd_probes)+" "+str(probab_real_final)
pasta_traces=gera_todos_traces(parametros_trace, qtd_traces)


def calcula_delta(probabilidades_estimadas):

    probabilidades_estimadas = [float(x) for x in probabilidades_estimadas]
    soma_das_diferencas_absolutas = 0

    for i in range (len(probabilidades_estimadas)-1):
        soma_das_diferencas_absolutas = soma_das_diferencas_absolutas + abs(probabilidades_estimadas[i] - probabilidades_estimadas[i+1])

    return soma_das_diferencas_absolutas / len(probabilidades_estimadas)



for i in range(1, qtd_traces+1):
    caminho_trace = pasta_traces+"/"+str(i)
    probabilidades_estimadas=executar_metodo(caminho_trace)
    linha=str(i)+","+metodo_e_parametros+","+probab_real_final+","+str(calcula_delta(probabilidades_estimadas))+"\n"
    with open("delta.csv", "a") as arquivo:
        arquivo.write(linha)







