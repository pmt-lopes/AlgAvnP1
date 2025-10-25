#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Maximum Subset Sum problem - Analysis of 2 approximation algorithms
1- A 2-approximation greed algorithm
2- A trim scheme algorithm with a approximation ratio of (1+epsilon)

Several instances of sets containing positive integers number, with different
sizes are created and tested for different target values, M, and epsilon values

The time of each algorithm is registered and their solution value are comparaded
with each other and in the cases that a known optimal value existes also
compared with it

To obtain the times the same inputs are repeated a number of times and 
an average and stdv values obtianed

Multiprocessing is used to compute this sampling in parallel

The data obtained is writen to a file

@author: Andre Wemans, 48432
@author: Pedro Lopes, 57514
"""

#%% Imports
import numpy as np
import sys
import time
import multiprocessing as mp

#Algorithm modules
import schemeSS as sss
import greddyMSS as gss
import setGenerator as sg

#%% Constants and hard coded parameters
cpus = 10 #To use 10 parallel workers
file_out = 'mss-data.txt'
file_instances = 'mss-instances.txt'
sizes = [10, 100] #instance sizes to be used
instance_repetition = 2 # number of instances to be used for each size
exact_sampling_ratio = 2 #How much elements should be summed to give obtained an exact M
rgn = np.random.default_rng() #Random generator
target_ratios = [.5, 1., 2.] #Ratios of exact value to use as M for each instance

#%% Functions
def write_instance(instance, file_pointer):
    '''Writes an instance to the file storing used instances
    instance: the set to be write to the file'''
    
    for j in range(instance.size-1):
        file_pointer.write(str(instance[j]) + '\t')
    #writes the last element
    file_pointer.write(str(instance[-1]) + '\n')
    

#%%Main program
if __name__ == '__main__':
    
    from_file = False #If the program should read the instances from a file
    
    if  len(sys.argv) == 2:
        #TODO: implement getting instances from file
        print('Warning: Reading instaces from a file not implemented.')
        
    #Initizalize workers pool and output files
    with mp.Pool(processes= cpus) as pool: 
        with  open(file_out, 'w') as fout:  
            with open(file_instances, 'w') as finst:
                
                for size in sizes:
                    for rept in range(instance_repetition):
                        
                        #Generates an instance of the given size
                        instance = sg.generator(size)
                        #Write instance to file
                        write_instance(instance, finst)
                        #Get instance information
                        max_value = instance[-1]
                        total_sum = instance.sum()
                        
                        #Gets a M value that gives a possible optimal solution
                        #It is needed that M / 2 > max_value
                        less_than = True
                        while less_than:
                            exact = rgn.choice(instance, size // exact_sampling_ratio, replace= False).sum()
                            less_than = ((exact / 2 ) < max_value)
                            
                        
