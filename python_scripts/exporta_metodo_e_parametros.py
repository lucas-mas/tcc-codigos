import sys
import os
import subprocess


sma="../simulators/sma"
ewma="../simulators/ewma"
hte="../simulators/hte"
htewma='../simulators/htewma'
htesw='../simulators/htesw'

#versao em python do hte. precisa ser otimizada (usar np.array em vez de lista built-in do python)
# htepy='../simulators/hte_py.py'

nome_metodo=sys.argv[1]

map_nome_caminho = {"hte": hte, "sma": sma, "ewma": ewma, "htewma": htewma, "htesw": htesw}

if nome_metodo == 'sma' or nome_metodo == 'ewma':
    parametros = [sys.argv[2]]
else:
    parametros = [sys.argv[2], sys.argv[3]]

caminho_metodo=map_nome_caminho[nome_metodo]


#o ultimo indice indica
#quando o parametro deixa de ser dados do metodo e passa a ser
#dados sobre o trace. ex.: hte 18 0.2 100 0.5 100 0.2.
#------------------ indice:|0 |1 | 2 | 3 | 4 | 5 | 6 |
#-------------------------|infos metodo: hte 18 0.2. indices 0, 1 e 2
#-------------------------| infos trace: 100 0.5 100 0.2. indices 3 4 5 e 6.
#-------------------------| 'ultimo_indice'=3
ultimo_indice=len(parametros)+1
trace_infos = sys.argv[ultimo_indice+1:]
#o indice da mudanca é a posicao do ultimo probe antes da probabilidade mudar
indice_mudanca = trace_infos[0]


str_parametros=' '.join(parametros)
executa_metodo=caminho_metodo+" "+str_parametros

probab_real_final=sys.argv[-1]



def executar_metodo(caminho_trace):
    script = "cat "+ caminho_trace+" | "+executa_metodo
    probabilidades_estimadas = subprocess.check_output(script, shell=True)
    probabilidades_estimadas = probabilidades_estimadas.decode('utf-8')
    probabilidades_estimadas = probabilidades_estimadas.split('\n')
    probabilidades_estimadas = [x for x in probabilidades_estimadas if x != '']
    return probabilidades_estimadas
