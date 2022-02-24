import os
import subprocess
import sys

#Edit this line adding the methods you want to evaluate. 
#The format should be: ["method_name" "parameters"]. 
#Each parameter must be separated by a space.
#Example: hte 18 0.1. Or sma 20
methods_to_evaluate = ['hte 18 0.1', 'sma 20']


if sys.argv[1] == 'conv':
    traces=[]
    for i in range(1, 10):
        for j in range(1, 10):
            trace1 = [500, i/10, 500, j/10]
            trace1 = [str(x) for x in trace1]
            traces.append(trace1)


    if not os.path.isfile('convergence.csv'):
        with open('convergence.csv', 'w') as file:
            line = 'method,Average convergence time (probes),Minimum,Maximum,ip,fp\n'
            file.write(line)
    for trace in traces:
        for method in methods_to_evaluate:
            script = 'python convergence_time.py'+' '+method+' '+' '.join(trace)
            subprocess.call(script, shell=True)


elif sys.argv[1] == 'delta' or sys.argv[1] == 'lambda':

    probabs = [x/10 for x in range(1, 10)]

    if sys.argv[1] == 'delta':
        file_csv = 'delta.csv'
        column_csv = 'Variability(Delta)'
        python_script = 'delta.py'
    elif sys.argv[1] == 'lambda':
        file_csv = 'lambda.csv'
        column_csv = 'Accuracy(Lambda)'
        python_script = 'calculate_accuracy.py'
        
    if not os.path.isfile(file_csv):
        with open(file_csv, 'w') as file:
            line = 'index,methods,p value,'+column_csv+'\n'
            file.write(line)
    for probab in probabs:
        for method in methods_to_evaluate:
            script = 'python '+python_script+" "+method+" "+str(probab)
            subprocess.call(script, shell=True)



