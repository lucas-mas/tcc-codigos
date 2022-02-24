import altair as alt
import pandas as pd
from altair_saver import save
import sys


#primeiro argumento é o file com os data
data = sys.argv[1]

if 'delta.csv' in sys.argv[1]:
    # y_axis_label = 'Variability'
    y_axis_label = 'Variability'
    y_axis_mean = 'mean(Variability(Delta)):Q'
    y_axis = 'Variability(Delta):Q'

elif 'lambda.csv' in sys.argv[1]:
    y_axis_label = 'Accuracy'
    # y_axis_label = 'Acurácia'
    y_axis_mean = 'mean(Accuracy(Lambda)):Q'
    y_axis = 'Accuracy(Lambda):Q'



source = pd.read_csv(data, sep=',')


source = source.replace({r'hteho ([0-9]+) (0.[0-9]+)': r'HTESW; w=\1; α=\2'}, regex=True)
source = source.replace({r'htewma (0.[0-9]+) (0.[0-9]+)': r'HTEWMA; β=\1; α=\2'}, regex=True)
source = source.replace({r'hte ([0-9]+) (0.[0-9]+)': r'HTE; w=\1; α=\2\n'}, regex=True)
source = source.replace({r'^ewma (0.[0-9]+)': r'EWMA; β=\1'}, regex=True)
source = source.replace({r'sma ([0-9]+)': r'SMA; w=\1'}, regex=True)
#Descomenta para o separador decimal ser vírgula em vez de ponto
# source = source.replace({'\.': ','}, regex=True)




point = alt.Chart(source).mark_point(size=5).encode(
    x=alt.X('p value:O', axis=alt.Axis(labelAngle=0), sort=None),
    y=alt.Y(y_axis_mean),
    # tooltip=[y_axis],
    color=alt.Color("methods:N")
)

line = alt.Chart(source).mark_line(strokeWidth=1).encode(
    x=alt.X('p value:O', axis=alt.Axis(labelAngle=0, title='p'), sort=None),
    y=alt.Y(y_axis_mean, axis=alt.Axis(title=y_axis_label)),
    color=alt.Color("methods:N", #scale=alt.Scale(scheme='set1'), 
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
    x=alt.X('p value:O', axis=alt.Axis(labelAngle=0, title='p'), sort=None),
    y=alt.Y(y_axis, axis=alt.Axis(title=y_axis_label)),
    color=alt.Color("methods:N",)
    # y=alt.Y('mean_delta:Q', axis=alt.Axis(title='Variability')),
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


