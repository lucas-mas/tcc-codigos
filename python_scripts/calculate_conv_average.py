import statistics
import math

#calculate o intervalo de confiança de 95%
#recebe como parâmetro a quantidade de amostras e o desvio padrão
def calculate_confidence_interval(n, dp):
    return 1.96 * (dp / math.sqrt(n))



def write_file(convergence_time_list, method_name, initial_probability, final_probability):
    average = statistics.mean(convergence_time_list)

    std_dev = statistics.stdev(convergence_time_list)
    confidence_interval = calculate_confidence_interval(len(convergence_time_list), std_dev)

    #caso a pessoa tenha passado só um file
    if len(convergence_time_list) == 1:
        std_dev = 0
        confidence_interval = 0

    else:
        std_dev = statistics.stdev(convergence_time_list)
        confidence_interval = calculate_confidence_interval(len(convergence_time_list), std_dev)

    with open("convergency.csv", "a") as file:
        line = method_name+','+str(average)+','+str(average-confidence_interval)+\
        ','+str(average+confidence_interval)+','+str(initial_probability)+','+str(final_probability)+'\n'
        file.write(line)