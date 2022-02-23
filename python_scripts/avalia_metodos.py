import os
import subprocess
import sys

# metodos_a_analisar = ['hte 18 0.1', 'htewma 0.1 0.1', 'sma 20', 'ewma 0.1', 'htesw 18 0.1']
metodos_a_analisar = ['hte 18 0.1', 'sma 20']


if sys.argv[1] == 'conv':
    traces=[]
    for i in range(1, 10):
        for j in range(1, 10):
            trace1 = [500, i/10, 500, j/10]
            trace1 = [str(x) for x in trace1]
            traces.append(trace1)


    if not os.path.isfile('convergencia.csv'):
        with open('convergencia.csv', 'w') as arquivo:
            linha = 'Metodo,Tempo de convergencia medio(em probes),Minimo,Maximo,pi,pf\n'
            arquivo.write(linha)
    for trace in traces:
        for metodo in metodos_a_analisar:
            script = 'python tempo_convergencia.py'+' '+metodo+' '+' '.join(trace)
            subprocess.call(script, shell=True)


elif sys.argv[1] == 'delta' or sys.argv[1] == 'lambda':

    probabs = [x/10 for x in range(1, 10)]

    if sys.argv[1] == 'delta':
        arquivo_csv = 'delta.csv'
        coluna_csv = 'Variabilidade(Delta)'
        python_script = 'delta.py'
    elif sys.argv[1] == 'lambda':
        arquivo_csv = 'lambda.csv'
        coluna_csv = 'Acuracia(Lambda)'
        python_script = 'acuracia_lambda.py'
        
    if not os.path.isfile(arquivo_csv):
        with open(arquivo_csv, 'w') as arquivo:
            linha = 'index,Metodos,Valor de p,'+coluna_csv+'\n'
            arquivo.write(linha)
    for probab in probabs:
        for metodo in metodos_a_analisar:
            script = 'python '+python_script+" "+metodo+" "+str(probab)
            subprocess.call(script, shell=True)



