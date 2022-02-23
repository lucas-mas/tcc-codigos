import math
import sys
import fileinput
import subprocess
from exporta_metodo_e_parametros import *
from calcula_media_conv import *
from gera_trace import *


args_lambda = nome_metodo+' '+' '.join(parametros) +' '+' '.join(trace_infos)

script = "python acuracia_lambda_convergencia.py "+args_lambda


lambda_medio = subprocess.check_output(script, shell=True)

lambda_medio = float(lambda_medio.decode())


qtd_traces = 300

parametros_trace=' '.join(trace_infos)
pasta_traces=gera_todos_traces(parametros_trace, qtd_traces)

exit()


def checa_se_convergiu(p_real, p_estimada, accuracy_lambda):
    #verifica se a probabilidade estimada está no intervalo [probab. estimada - lambda, probab_estimada + lambda]
    return abs(p_real - p_estimada) <= accuracy_lambda


def calcula_tempo_convergencia(nova_probabilidade, probabilidades_estimadas, accuracy_lambda, indice_da_mudanca):
    nova_probabilidade = float(nova_probabilidade)
    indice_da_mudanca = int(indice_da_mudanca)
    probabilidades_estimadas = [float(x) for x in probabilidades_estimadas]
    tempo_convergencia = 0
    #o for começa a partir do momento em que a probabilidade mudou
    for i in range(indice_da_mudanca, len(probabilidades_estimadas)):
        #se convergiu, para o loop
        if checa_se_convergiu(nova_probabilidade, probabilidades_estimadas[i], accuracy_lambda):
            break

        tempo_convergencia += 1


    return tempo_convergencia





lista_tempos_convergencia = []
for i in range(1, qtd_traces+1):
    caminho_trace = pasta_traces+"/"+str(i)
    probabilidades_estimadas=executar_metodo(caminho_trace)
    conv = calcula_tempo_convergencia(probab_real_final, probabilidades_estimadas, lambda_medio, int(indice_mudanca))
    lista_tempos_convergencia.append(conv)


pi = trace_infos[1]
pf = trace_infos[-1]

nome_metodo_completo = nome_metodo+' ' + ' '.join(parametros)

escreve_arquivo(lista_tempos_convergencia, nome_metodo_completo, pi, pf)