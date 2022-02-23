
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



def calcula_lambda(probabilidades_estimadas, probabilidade_real):

    probabilidades_estimadas = [float(x) for x in probabilidades_estimadas]

    soma_das_diferencas_absolutas = 0

    for i in range (len(probabilidades_estimadas)-1):
        soma_das_diferencas_absolutas = soma_das_diferencas_absolutas + abs(probabilidades_estimadas[i] - probabilidade_real)

    return (soma_das_diferencas_absolutas / len(probabilidades_estimadas))


lambda_total = 0
for i in range(1, qtd_traces+1):
    caminho_trace = pasta_traces+"/"+str(i)
    probabilidades_estimadas=executar_metodo(caminho_trace)
    lambda_total=lambda_total + calcula_lambda(probabilidades_estimadas, float(probab_real_final))

lambda_media = lambda_total / qtd_traces

print(lambda_media)

