

import altair as alt
import pandas as pd
from altair_saver import save
import os
import sys


#primeiro argumento é o arquivo com os dados
dados = sys.argv[1]

if 'delta.csv' in sys.argv[1]:
    # eixo_y_label = 'Variabilidade'
    eixo_y_label = 'Variability'
    eixo_y_mean = 'mean(Variabilidade(Delta)):Q'
    eixo_y = 'Variabilidade(Delta):Q'

elif 'lambda.csv' in sys.argv[1]:
    eixo_y_label = 'Accuracy'
    # eixo_y_label = 'Acurácia'
    eixo_y_mean = 'mean(Acuracia(Lambda)):Q'
    eixo_y = 'Acuracia(Lambda):Q'



source = pd.read_csv(dados, sep=',')


source = source.replace({r'hteho ([0-9]+) (0.[0-9]+)': r'HTESW; w=\1; α=\2'}, regex=True)
source = source.replace({r'htewma (0.[0-9]+) (0.[0-9]+)': r'HTEWMA; β=\1; α=\2'}, regex=True)
source = source.replace({r'hte ([0-9]+) (0.[0-9]+)': r'HTE; w=\1; α=\2\n'}, regex=True)
source = source.replace({r'^ewma (0.[0-9]+)': r'EWMA; β=\1'}, regex=True)
source = source.replace({r'sma ([0-9]+)': r'SMA; w=\1'}, regex=True)
#Descomenta para o separador decimal ser vírgula em vez de ponto
# source = source.replace({'\.': ','}, regex=True)




point = alt.Chart(source).mark_point(size=5).encode(
    x=alt.X('Valor de p:O', axis=alt.Axis(labelAngle=0), sort=None),
    y=alt.Y(eixo_y_mean),
    # tooltip=[eixo_y],
    color=alt.Color("Metodos:N")
)

line = alt.Chart(source).mark_line(strokeWidth=1).encode(
    x=alt.X('Valor de p:O', axis=alt.Axis(labelAngle=0, title='p'), sort=None),
    y=alt.Y(eixo_y_mean, axis=alt.Axis(title=eixo_y_label)),
    color=alt.Color("Metodos:N", #scale=alt.Scale(scheme='set1'), 
    legend=\
        alt.Legend(
        columns=1,
        title="",
        orient='right',
        labelFontSize=13,
        titleFontSize=15,
        direction='horizontal',
        ))
)


band = alt.Chart(source).mark_errorbar(extent='ci').encode(
    x=alt.X('Valor de p:O', axis=alt.Axis(labelAngle=0, title='p'), sort=None),
    y=alt.Y(eixo_y, axis=alt.Axis(title=eixo_y_label)),
    color=alt.Color("Metodos:N",)
    # y=alt.Y('mean_delta:Q', axis=alt.Axis(title='Variabilidade')),
)


chart = alt.layer(
    point,#.mark_point(),
    line,#.mark_line(),
    band#.mark_errorbar(extent='ci')
).properties(
    width=375,
    height=220
).configure_point(
    # size=100,
    filled=True
).configure_axis(
    labelFontSize=15,
    titleFontSize=15
)

#o -4 eh para tirar o .csv do final da string.
if sys.argv[2] == "s":
    chart.save(sys.argv[1][:-4]+'.png', scale_factor=3)

elif sys.argv[2] == 'i':
    chart.interactive().save(sys.argv[1]+'.html')


