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
sizes = [10, 100, 1000, 10000] #instance sizes to be used
instance_repetition = 2 # number of instances to be used for each size
exact_sampling_ratio = 2 #How much elements should be summed to give obtained an exact M
rgn = np.random.default_rng() #Random generator
target_ratios = [.5, 1, 2] #Ratios of exact value to use as M for each instance
epsilon = [0.5, 1, 2]
#%% Functions
def write_line_to_file(line, file_pointer):
    '''Writes an instance to the file storing used instances
    instance: the set to be write to the file'''
    
    for j in range(len(line)-1):
        file_pointer.write(str(line[j]) + '\t')
    #writes the last element
    file_pointer.write(str(line[-1]) + '\n')
    
def extrac_data(data):
    '''Extracts time and value data from algorithms output
    data: 2D list with (t, value) from each process
    
    Issues warning if all values are not indentical
    
    return: t_average, t_stdv, value'''
    
    #Computes value and time average and stdv
    data = np.array(data)
    t = data[:, 0] #Getting times
    values = data[:, 1] #Getting values
    
    t_average = np.mean(t)
    t_stdv = np.std(t, ddof= 1)
    
    value = values[0]
    #Check if all values are the same
    if not np.all(values == value):
        print('Warning: Differen values between processess')
        
    return t_average, t_stdv, value
    
#%%Main program
if __name__ == '__main__':
    
    from_file = False #If the program should read the instances from a file
    
    if  len(sys.argv) == 2:
        #TODO: implement getting instances from file
        print('Warning: Reading instaces from a file not implemented.')
        
    count = 0 #Sample counter
        
    #Initizalize workers pool and output files
    with mp.Pool(processes= cpus) as pool: 
        with  open(file_out, 'w') as fout:  
            with open(file_instances, 'w') as finst:
                
                data_header = ['Sample', 'Size', 'Max Value', 'Total sum', 'M', 'Exact?', 'Algorithm', 
                               'epsilon', 'Value', 'Value / M', 't', 't stdv']
                write_line_to_file(data_header, fout)
                
                for size in sizes:
                    for rept in range(instance_repetition):
                        
                        #Generates an instance of the given size
                        instance = sg.generator(size)
                        #Write instance to file
                        write_line_to_file(instance, finst)
                        #Get instance information
                        max_value = instance[-1]
                        total_sum = instance.sum()
                        
                        #Gets a M value that gives a possible optimal solution
                        #It is needed that M / 2 > max_value
                        less_than = True
                        while less_than:
                            exact = rgn.choice(instance, size // exact_sampling_ratio, replace= False).sum()
                            less_than = ((exact / 2 ) < max_value)
                        
                            
                        
                        for r_value in target_ratios:
                            
                            #Text base to output for data file
                            count += 1
                            text_out_base = [count, size, max_value, total_sum]
                            
                            M = int(r_value * exact)
                            
                            is_exact = (r_value == 1)
                            #Register target value
                            text_out_base = text_out_base + [M]
                            #Register if it is an exact solution or if it is unknown
                            if is_exact:
                                text_out_base += ['E']
                            else:
                                text_out_base += ['U']
                            
                            #Computes value and time
                            data = pool.starmap(gss.greedySS2_timed, cpus * [[instance, M]])
                            t_average, t_stdv, value = extrac_data(data)
                            #Add to the data line the remaining data
                            text_out = text_out_base +  ['G', '-', value, value / M, t_average, t_stdv]
                            
                            #Write data to file
                            write_line_to_file(text_out, fout)
                            
                            
                            text_out_base_SS = text_out_base + ['S']
                            
                            #Computes time and value using scheme algorithm
                            for e in epsilon:
                               	count += 1
                               	text_out_base_SS[0] = count
                                text_out = text_out_base_SS + [e]
                                data = pool.starmap(sss.schemeSS_val_timed, cpus * [[instance, M, e]])
                                
                                t_average, t_stdv, value = extrac_data(data)
                                #Add to the data line the remaining data
                                text_out += [value, value / M, t_average, t_stdv]
                                
                                #Write data to file
                                write_line_to_file(text_out, fout)
