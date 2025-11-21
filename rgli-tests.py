#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests the RGLI algorithm considering how close to the target value, M,
it can achieve after the random phase, and after the local improvement, which
is deterministic.

Also tests the evaluation of the solution value with the number of repetitions

@author: Andre Wemans, 48432
@author: Pedro Lopes, 57514
"""
#%% Imports
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import RGLI as rgli
import time
import multiprocessing as mp
#%% Constants
iterations = 500
individual_rep = 50
data_file = 'mss-data-0.txt'
instances_file = 'mss-instances-0.txt'
lines_to_remove = 1
cpus = 10
data_out_file = 'rgli-analysis-data.txt'
#%% Load mss-data as a dataframe
data = pd.read_csv(data_file, sep= '\t')

#Reomve the last lines due to incomplete data
data = data.iloc[:- lines_to_remove]

#%% Load instances
with open(instances_file, 'r') as file:
    
    instances = []
    
    csv_file = csv.reader(file, delimiter= '\t')
    
    for line in csv_file:
        instances.append(line)
    
    #convert the instances information in integeres and drop the last
    #one because it was not used and there is no information concerning
    #M value
    for i in range(len(instances) - 1):
        instances[i] = [int(j) for j in instances[i]]

#filters data just for the rgli algorithm
data_rgli = data[data['Algorithm'] == 'R']

#Gets the M values for each test, there are 3 different M values for
#each instance
M_values = data_rgli['M']

#%%Applies the RGLI algorithm to all instances and collects data
if __name__ == '__main__':
    count = 0
    t0 = time.time_ns()
    random_values = []
    out_values = []
    with mp.Pool(processes= cpus) as pool:
        for i, instance in enumerate(instances):
            for M in M_values[3 * i: 3 * (i + 1)]:
                output = []
                values = []
                
                for rep in range(iterations):
                    sol, value, remaining = rgli.randomGreedy_threadSafe(instance, M)
                    output.append([sol, value, remaining, M])
                    values.append(value)
                ratio = np.array(values) / M
                
                random_values.append([i + 1, len(instance), iterations, 
                                      M, ratio.mean(), ratio.std(ddof = 1)])
                
                li_values = pool.starmap(rgli.localImprovement_sol,
                    output)
                
                #Checking for each sample the difference between value
                #from random and after local improvement
                improvement = np.array([[i + 1, len(instance), v, li, li / v, v/M, li/M] 
                               for v, li in zip(values, li_values)])
                
                li_ratio = improvement[:, 3] / M
                
                li_random_ratio = li_ratio / ratio
                
                #Considering the algorithm making 50 repetitions for each
                #sampling, how many repetitions for each sampling were performed
                #in average until the maximum value were obtained
                li_values = np.array(li_values)
                maximum_index = []
                for j in range(len(li_values) // individual_rep):
                    
                    sampling = li_values[j * individual_rep :
                                         (j + 1) * individual_rep]
                    v0 = 0
                    for k, k_sample in enumerate(sampling):
                        if k_sample > v0:
                            v0 = k_sample
                            ind = k
                    
                    maximum_index.append(ind)
                    
                max_ind = np.array(maximum_index)
                out_values.append([i + 1, len(instance), iterations, 
                                      M, ratio.mean(), ratio.std(ddof= 1),
                                      li_ratio.mean(), 
                                      li_ratio.std(ddof= 1), 
                                      li_random_ratio.mean(),
                                      li_random_ratio.std(ddof= 1),
                                      max_ind.mean(),
                                      max_ind.std(ddof= 1)])
                
                count += 1 
                print(count)
    values_df = pd.DataFrame(out_values, columns= ['Instance', 'intance size', 
                        '# samples', 'M', 'Mean random value/M', 
                        'std random value/M', 'Mean li value/M', 'std li value/M',
                        'Mean (li/random)', 'std (li/random)',
                        'Index of maximum mean', 'Index of maximum std'])
    
    
    t1 = time.time_ns()
    
    print((t1-t0) * 10**-9)
    
    values_df.to_csv(data_out_file, sep= '\t')