#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implements the greedySS2 algorithm from pratical class 2
for solving a maximum subset-sum problem

Receives a set of numbers and a value and gives a approximation
to the maximum sum of elements of a subset equal or less than the value

@author: Andre Wemans, 48432
@author: Pedro Lopes, 57514
"""
#%% Imports
import numpy as np
from setGenerator import *
from schemeSS import *
import schemeSS_fast as ss
import time
#%% functions
def greedySS2(instance, value):
    '''Implements a 2-aproach algorithm for solving the problem of
    Maximum Subset Sum, given a set of integer and positive values
    computes a solution with a subset-value <= value and the correspondet
    subset.
    instance: the ordered set with the numbers
    value: the goal value for the sum of elements in the subset to be less or
    equal. It is assumed that value > max(elements of instance)
    
    out: sum-> intger with the sum of the elements in the subset, subset->
    subset obtained by the algorith'''
    
    sol= [] #list to store solution
    v = 0 #intial subset value
    
    #cycling through all elements
    for el in instance:
        #if by adding a new element the new sum is less or equal than the target value
        if v + el <= value:
            sol += [el] #adds the element to the solution
            v += el #adds the element value to the subset sum
            
    #if the adding a new element the new sum is higher than the target value
    else:
        #if the sum so far obtained is higher than the element being tested
        if v >= el:
            return v, sol
        #if the element being tested is higher than the sum obtained so far
        else:
            return el, [el]
#%% testing
if __name__ == '__main__':
    #creates an instance
    instance = generator(1000)
    max_value = max(instance)
    total_sum = sum(instance)
    
    rgn = np.random.default_rng()
    exact = rgn.choice(instance, 500, replace= False).sum()
    print(exact)
    print(max_value, total_sum)
    
    r = [.1, .2, .5, 1., 2.]
    for f in r:
        print('factor to exact of: ', f)
        print('Target value: ', f * exact)
        if exact < total_sum and exact > max_value:
            t0 = time.time_ns()
            s, sol = greedySS2(instance, f * exact)
            t1 = time.time_ns()
            print(s)
            print("Total time: {} s".format((t1 - t0) / 10 ** 9))
            print('Appr: ', s / (f * exact))
            tg = t1-t0
            
            t0 = time.time_ns()
            s, _ = schemeSS(instance, f * exact, .1)
            t1 = time.time_ns()
            print(s)
            print("Total time: {} s".format((t1 - t0) / 10 ** 9))
            print('Appr: ', s / (f * exact))
            ta1 = t1 - t0
            
            
            t0 = time.time_ns()
            s, _ = ss.schemeSS_optimized(instance, f * exact, .1)
            t1 = time.time_ns()
            print(s)
            print("Total time: {} s".format((t1 - t0) / 10 ** 9))
            print('Appr: ', s / (f * exact))
            ta2 = t1 - t0
            
            print('ta1 / tg', ta1 / tg)
            print('ta2 / tg', ta2 / tg)
            print('ta1 / ta2', ta1 / ta2)
