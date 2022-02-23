import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import altair as alt
import pandas as pd
from altair_saver import save
import fileinput
from exporta_metodo_e_parametros import *
from gera_trace import *

qtd_traces=1


metodo = nome_metodo+'-' + '-'.join(parametros)

parametros_trace=' '.join(trace_infos)
pasta_traces=gera_todos_traces(parametros_trace, qtd_traces)



def gera_grafico(probabilidades_estimadas, index):
    source = {'p': probabilidades_estimadas, 'probes': [x for x in range (1, len(probabilidades_estimadas)+1)]}


    source = pd.DataFrame(source)

    chart = alt.Chart(source).mark_line().encode(
        x=alt.X('probes', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('p', title="estimativa de p"),
    ).properties(width=660, height=200).interactive()


    nome=metodo+'.'+str(index)+".png"
    chart.save(nome)


for i in range(1, qtd_traces+1):
    caminho_trace=pasta_traces+'/'+str(i)
    probabilidades_estimadas = executar_metodo(caminho_trace)
    probabilidades_estimadas = [float(x) for x in probabilidades_estimadas]
    gera_grafico(probabilidades_estimadas, i)