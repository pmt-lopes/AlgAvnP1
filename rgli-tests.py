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
#%% Constants
iterations = 500
data_file = 'mss-data-0.txt'
instances_file = 'mss-instances-0.txt'
lines_to_remove = 1

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
count = 0
t0 = time.time_ns()
random_values = []
for i, instance in enumerate(instances):
    for M in M_values[3 * i: 3 * (i + 1)]:
        output = []
        values = []
        
        for rep in range(iterations):
            sol, value, remaining = rgli.randomGreedy_threadSafe(instance, M)
            output.append([sol, value, remaining])
            values.append(value)
        ratio = np.array(values) / M
        
        random_values.append([i + 1, len(instance), iterations, 
                              M, ratio.mean(), ratio.std(ddof = 1)])
        count += 1 
        print(count)
randm_values_df = pd.DataFrame(random_values, columns= ['Instance', 'intance size', 
                    '# samples', 'M', 'Mean value/M', 'std value/M'])
t1 = time.time_ns()

print((t1-t0) * 10**-9)