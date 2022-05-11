# tcc-scripts
Scripts used to analyze HTE, HTEWMA, HTESW, SMA and EWMA convergence time.

**"simulators" folder:**

Numerical simulators for the five methods.

**"python_scripts" folder:**

Scripts developed to analyze the performance of these methods.

- Accuracy gap calculatetor
- Variability calculatetor
- Convergence time calculator
- Accuracy gap, variability and convergence time graph generators
- And some others

----


**1 How to use the script to generate analysis on the methods**

The evaluate_methods.py script is used to evaluate methods on the three measures: accuracy gap, variability and convergence time. This script takes as a parameter the measure you want to evaluate the methods. Only this script needs to be used to generate a file with the results of the methods, as it calls the other necessary helper scripts (for example, it generates the necessary traces to evaluate the methods). Following are the options that can be passed as a parameter.

Evaluate convergence time: "conv"
Evaluate variability: "delta"
Evaluate accuracy gap: "lambda"

For example, to assess accuracy gap, the script should be called like this:

python evaluate_methods.py lambda

To define which methods should be evaluated, the value of the methods_to_evaluate variable must be edited. This variable is a list of strings, and each string is a method with its parameters. For example, if you want to analyze HTE with alpha 0.1 and window w = 20, you would add the string "hte 20 0.1" to the list. The format that should be used in the string passed as a parameter to each method is shown below, where w is a window size, α is an alpha value, and β is a beta value.

hte w α

sma w

ewma β

htewma β α

htesw w α


Running the script following these instructions will generate a .csv file with the results. The structure of the generated .csv file will be detailed below.

**2 Explanation of the structure of the generated .csv files**

**2.1 Convergence time**

The following table shows the meaning of each column of the generated .csv file when evaluating the convergence time of the methods.



| Column                            | Meaning                                         |
|-----------------------------------|-------------------------------------------------|
| method                            | Method evaluated                                |
| Average convergence time (probes) | Calculated average convergence time             |
| Maximum                           | Mean convergence time minus confidence interval |


For each combination of ip and fp, 300 traces are generated with the same characteristics so that the convergence time is measured 300 times and the mean and confidence interval are calculated, thus returning a statistically more relevant result. The data recorded in the .csv file is the mean (Average convergence time(probes) column), plus the minimum and maximum limits of the confidence interval (Minimum and Maximum columns, respectively).
 
For each parameterized method considered, the convergence times are calculated considering 81 different scenarios, since the ip value varies from 0.1 to 0.9 with increments of 0.1 and, for each ip value, the values fp ranging from 0.1 to 0.9 in increments of 0.1. Each of these 81 scenarios is recorded as a line in the .csv file.

In each of the combinations between ip and fp, the trace used has 1000 probes: the first 500 probes with the initial probability of success (ip) and the last 500 probes with the final probability of success (fp). For example, with ip = 0.3 and fp = 0.9, a trace is generated with the first 500 probes with p = 0.3 and the last 500 probes with p = 0.9.

**2.2 Delta and Lambda**

The following table shows the meaning of each column of the .csv file generated when evaluating the lambda of the methods.

| Column               | Meaning                       |
|----------------------|-------------------------------|
| method               | Method evaluated              |
| p value              | Actual probability of success |
| Accuracy gap(lambda) | Average accuracy gap          |

The following table shows the meaning of each column of the generated .csv file when evaluating the delta of the methods.

| Column             | Meaning                       |
|--------------------|-------------------------------|
| method             | Method evaluated              |
| p value            | Actual probability of success |
| Variability(delta) | Average variability           |


For each parameterized method being evaluated, the measurement result (delta or lambda) is calculated considering 9 final probabilities of success: from 0.1 to 0.9, with increments of 0.1. For each of these 9 probabilities, 10 lines are generated in the .csv file, as 10 different traces with the same characteristics are used. For example, for the true probability of success 0.3, 10 different traces are generated with 200000 probes each, and each probe has a 30% probability of being 1. This approach of generating 10 traces was chosen so that a mean of the method result considering the 10 traces and calculate the confidence interval, thus returning statistically more relevant results.

**3 How traces are generated**

The generate_trace.py file has the logic for generating the traces. The generation of a trace is done as follows. We use the numpy library's random.binomial method to randomly select the number 0 or 1. This number represents the packet (probe) received or lost. That is, there is no dependency between the consecutive packets received, and the size of the considered packet is always the same, since in this abstraction the packet is represented only by the numbers 0 and 1.

It is not necessary to generate the traces manually, as the evaluate_methods.py script already calls the necessary scripts to use existing traces or generate new ones, if necessary. We will explain in general how the generation of traces is.

The generate_trace.py script contains the methods that build the traces needed to evaluate the methods. The main method of the script is generate_all_traces. The other methods present in the script are helpers, and help to assemble each piece of the trace. The working logic of this main method will be explained below.

**generate_all_traces(trace_parameters, number_of_traces)**

**trace_parameters**: is a string that represents the characteristics you want the trace to have. For example, if you want the trace to have 800 probes, with the first 500 probes having a success probability of 0.1 and the last 300 probes having a success probability of 0.2, this variable should have the value "500 0.1 300 0.2".

**number_of_traces**: indicates the number of traces that must be generated. For example, if this variable has the value 100, 100 traces will be generated with the same characteristics defined in the trace_parameters variable. This repetition of traces is useful so that it is possible to calculate the average performance of the methods (and the confidence interval) when evaluating each of the three measures (accuracy gap, variability and time of convergence), thus returning statistically more relevant results.

**Return**: the generate_all_traces method creates a folder that stores all created traces. For example, if the number_of_traces variable is 100, these 100 traces are in this created folder. This folder is located a directory above where the generate_trace.py script is, inside a folder named “traces”. The return of the generate_all_traces method is the relative path to this created folder.
