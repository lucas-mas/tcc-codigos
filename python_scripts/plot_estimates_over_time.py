import pandas as pd
import altair as alt
from altair_saver import save
from export_method_and_parameters import *
from generate_trace import *

number_of_traces=1


method = method_name+'-' + '-'.join(parameters)

trace_parameters=' '.join(trace_infos)
traces_folder=generate_all_traces(trace_parameters, number_of_traces)



def generate_plot(estimated_probabilities, index):
    source = {'p': estimated_probabilities, 'probes': [x for x in range (1, len(estimated_probabilities)+1)]}


    source = pd.DataFrame(source)

    chart = alt.Chart(source).mark_line().encode(
        x=alt.X('probes', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('p', title="estimativa de p"),
    ).properties(width=660, height=200).interactive()


    name=method+'.'+str(index)+".png"
    chart.save(name)


for i in range(1, number_of_traces+1):
    trace_file_path=traces_folder+'/'+str(i)
    estimated_probabilities = run_method(trace_file_path)
    estimated_probabilities = [float(x) for x in estimated_probabilities]
    generate_plot(estimated_probabilities, i)