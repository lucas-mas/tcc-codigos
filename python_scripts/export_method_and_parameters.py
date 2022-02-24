import sys
import subprocess


sma="../simulators/sma"
ewma="../simulators/ewma"
hte="../simulators/hte"
htewma='../simulators/htewma'
htesw='../simulators/htesw'

#versao em python do hte. precisa ser otimizada (usar np.array em vez de list built-in do python)
# htepy='../simulators/hte_py.py'

method_name=sys.argv[1]

map_name_path = {"hte": hte, "sma": sma, "ewma": ewma, "htewma": htewma, "htesw": htesw}

if method_name == 'sma' or method_name == 'ewma':
    parameters = [sys.argv[2]]
else:
    parameters = [sys.argv[2], sys.argv[3]]

method_path=map_name_path[method_name]


#o ultimo indice indica
#quando o parametro deixa de ser data do method e passa a ser
#data sobre o trace. ex.: hte 18 0.2 100 0.5 100 0.2.
#------------------ indice:|0 |1 | 2 | 3 | 4 | 5 | 6 |
#-------------------------|infos method: hte 18 0.2. indices 0, 1 e 2
#-------------------------| infos trace: 100 0.5 100 0.2. indices 3 4 5 e 6.
#-------------------------| 'trace_infos_first_position'=3
trace_infos_first_position=len(parameters)+2
trace_infos = sys.argv[trace_infos_first_position:]
#o indice da mudanca é a posicao do ultimo probe antes da probabilidade mudar
first_new_probability_position = trace_infos[0]


str_parameters=' '.join(parameters)
method_path_and_parameters=method_path+" "+str_parameters

final_real_probability=sys.argv[-1]



def run_method(trace_file_path):
    script = "cat "+ trace_file_path+" | "+method_path_and_parameters
    estimated_probabilities = subprocess.check_output(script, shell=True)
    estimated_probabilities = estimated_probabilities.decode('utf-8')
    estimated_probabilities = estimated_probabilities.split('\n')
    estimated_probabilities = [x for x in estimated_probabilities if x != '']
    return estimated_probabilities
