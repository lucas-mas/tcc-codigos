import subprocess
from export_method_and_parameters import *
from calculate_conv_average import *
from generate_trace import *


args_lambda = method_name+' '+' '.join(parameters) +' '+' '.join(trace_infos)

scrinitial_probabilityt = "python calculate_accuracy_for_convergency.py "+args_lambda


average_lambda = subprocess.check_output(scrinitial_probabilityt, shell=True)

average_lambda = float(average_lambda.decode())

#The average accuracy time will be calculated based on this total traces.
#Here the quantity of generated traces can be modified.
number_of_traces = 10

trace_parameters=' '.join(trace_infos)
traces_folder=generate_all_traces(trace_parameters, number_of_traces)


def check_if_converged(p_real, p_estimada, accuracy_lambda):
    #verifica se a probabilidade estimada está no intervalo [probab. estimada - lambda, probab_estimada + lambda]
    return abs(p_real - p_estimada) <= accuracy_lambda


def calculate_convergency_time(nova_probabilidade, estimated_probabilities, accuracy_lambda, first_new_probability_position):
    nova_probabilidade = float(nova_probabilidade)
    first_new_probability_position = int(first_new_probability_position)
    estimated_probabilities = [float(x) for x in estimated_probabilities]
    convergency_time = 0
    #o for começa a partir do momento em que a probabilidade mudou
    for i in range(first_new_probability_position, len(estimated_probabilities)):
        #se convergiu, para o loop
        if check_if_converged(nova_probabilidade, estimated_probabilities[i], accuracy_lambda):
            break

        convergency_time += 1


    return convergency_time





list_convergency_time = []
for i in range(1, number_of_traces+1):
    trace_file_path = traces_folder+"/"+str(i)
    estimated_probabilities=run_method(trace_file_path)
    conv = calculate_convergency_time(final_real_probability, estimated_probabilities, average_lambda, int(first_new_probability_position))
    list_convergency_time.append(conv)


initial_probability = trace_infos[1]
final_probability = trace_infos[-1]

method_and_parameters = method_name+' ' + ' '.join(parameters)

write_file(list_convergency_time, method_and_parameters, initial_probability, final_probability)