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
#%% Constants
iterations = 50
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

#%%Applies the RGLI algorithm to all instances and collects data


for i, instance in enumerate(instances):
    pass