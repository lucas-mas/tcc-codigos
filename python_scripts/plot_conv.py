from typing import final
import altair as alt
from altair.vegalite.v4.schema.channels import Opacity
from altair.vegalite.v4.schema.core import ColorScheme, TickConfig
import pandas as pd
from altair_saver import save
import sys

# y_axis_label = 'Tempo de convergência médio (em probes)'
# pi = 'pi'
# pf = 'pf'
methods_legend_color='method'

y_axis_label = 'Average convergence time (probes)'
pi_label = "ip"
pf_label = "fp"
methods_legend_color='Method'


data = sys.argv[1]

source = pd.read_csv(data, sep=',')


maior_valor = max(source['Maximum'])


#aqui só ajeita os names dos métodos para que os parâmetros deles apareçam nas legendas
source = source.replace({r'hteho ([0-9]+) (0.[0-9]+)': r'HTESW; w=\1; α=\2'}, regex=True)
source = source.replace({r'htewma (0.[0-9]+) (0.[0-9]+)': r'HTEWMA; β=\1; α=\2'}, regex=True)
source = source.replace({r'hte ([0-9]+) (0.[0-9]+)': r'HTE; w=\1; α=\2\n'}, regex=True)
source = source.replace({r'^ewma (0.[0-9]+)': r'EWMA; β=\1'}, regex=True)
source = source.replace({r'sma ([0-9]+)': r'SMA; w=\1'}, regex=True)
#Separador decimal virgula em vez de ponto
# source = source.replace({'\.': ','}, regex=True)

if sys.argv[2] == "menos":
    # deixa só pi = 0.2, 0.5 e 0.8.
    indexNames = source[source['pi'].isin([0,1, 0.1, 0,3, 0.3, 0,4, 0.4, 0,6, 0.6, 0,7, 0.7, 0,9, 0.9])].index
    source = source.drop(indexNames)

print(source)

error_bars = alt.Chart(source).mark_errorbar().encode(
        x=alt.X('pf:N'),
        y=alt.Y('Minimum:Q', title=''),
        y2='Maximum:Q',
        color=alt.Color('method:N', title=methods_legend_color), #scale=alt.Scale(scheme='set1'),

    )

tick_baixo = alt.Chart(source).mark_tick(size=5).encode(
x=alt.X('pf:N', axis=alt.Axis(labelAngle=0), sort=None),
y=alt.Y('Minimum', title=''),
color=alt.Color('method:N',), #scale=alt.Scale(scheme='set1'),

)

tick_alto = alt.Chart(source).mark_tick(size=5).encode(
x=alt.X('pf:N', axis=alt.Axis(labelAngle=0), sort=None),
y=alt.Y('Maximum',),
color=alt.Color('method:N',), #scale=alt.Scale(scheme='set1'),

)

chart = alt.Chart(source).mark_line(point=True, strokeWidth=1.2).encode(
    x=alt.X('pf:O', axis=alt.Axis(title=pf_label,labelAngle=0, tickMinStep=0.3), sort=None),
    y=alt.Y('Average convergence time (probes):Q', axis=alt.Axis(labelFontSize=14), scale=alt.Scale(domain=[0, maior_valor],),title=y_axis_label), #0.1 = 500, 0.1 janela pequena = 260, 0.6 = 190
    color=alt.Color('method:N',
    legend=alt.Legend(
        orient='right',
        # orient='bottom',
        # title="aasdasd",
        columns=1,
        labelFontSize=13,
        # titleFontSize=15,
        # direction='vertical',
        # legendX=500,
        # legendY=1200,
        # titleAnchor='middle',
        ),
        ),
    
    opacity=alt.value(0.9),
    shape=alt.Shape('method:N', legend=None),
    # facet=alt.Facet('pi:N', columns=3),
    tooltip=['Average convergence time (probes):Q'],    
)
#\
# .configure_point(
#     size=50
# ).resolve_axis(
#     x='independent',
#     y='independent',)



chart = alt.layer(chart, error_bars, tick_alto, tick_baixo)\
    .properties(width=150, height=150)\
    .facet(alt.Facet('pi:N', title=pi_label,),columns=3)\
    .properties(
    # width=375,
    # height=220
    # width=150,
    # height=150
    # title='abvsfasdfas'
     )\
    .configure_point(size=20)\
    .resolve_axis(
        x='independent',
        # x=alt.X('pf:Q', axis=alt.Axis(tickMinStep=0.3)),
    # y='independent',
    ).resolve_scale(
    # color='independent',
    # shape='independent'
).configure_axis(
    labelFontSize=12,
    titleFontSize=13,
)


chart.save(sys.argv[1]+'.png', scale_factor=3)
