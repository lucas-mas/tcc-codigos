import numpy as np
from export_method_and_parameters import *
from generate_trace import *


number_of_probes=200000

#The average accuracy time will be calculated based on this total traces.
#Here the amount of traces considered in the average calculation can be modified.
number_of_traces = 10

method_and_parameters=method_name+" "+' '.join(parameters)


trace_parameters=str(number_of_probes)+" "+str(final_real_probability)
traces_folder=generate_all_traces(trace_parameters, number_of_traces)



def calculate_lambda(estimated_probabilities, real_probability):

    estimated_probabilities = [float(x) for x in estimated_probabilities]

    sum_of_absolute_differences = 0

    for i in range (len(estimated_probabilities)-1):
        sum_of_absolute_differences = sum_of_absolute_differences + abs(estimated_probabilities[i] - real_probability)

    return (sum_of_absolute_differences / len(estimated_probabilities))



for i in range(1, number_of_traces+1):
    trace_file_path = traces_folder+"/"+str(i)
    estimated_probabilities=run_method(trace_file_path)
    line=str(i)+","+method_and_parameters+","+final_real_probability+","+str(calculate_lambda(estimated_probabilities, float(final_real_probability)))+"\n"
    with open("lambda.csv", "a") as file:
        file.write(line)