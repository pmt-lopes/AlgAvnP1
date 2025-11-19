#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implements the randomized greedy with local improvement (RGLI) from
reference ,
for solving a maximum subset-sum problem using triming the solutuins
that are closer to a factor of each other

Receives a set of numbers, a value and the trimming factor 
and gives a approximation to the maximum sum of elements of a subset equal or 
less than the value

@author: Andre Wemans, 48432
@author: Pedro Lopes, 57514
"""

import sys
import random
import csv
import time

def randomGreedy(S, M):
    randomS = list(S)
    random.shuffle(randomS)

    sol = []
    sum = 0

    for el in randomS:
        if sum + el < M:
            sol += [el]
            sum += el
    
    remaining = list(set(S) - set(sol))
    remaining.sort()
    return sol, sum, remaining

def filterFunction(el, r, error):
    bigger = r > el # Element in remaining has to be bigger to have an improvement
    diff = r - el
    valid = diff <= error # Difference can't exceed bound of the sum 

    return bigger & valid

def localImprovement(Sol, sum, remaining, M):

    improvedSol = list(Sol)
    improvedSum = sum
    
    if sum == M:
        return Sol, sum
    
    error = M - sum
    
    for el in Sol:
        replacements = [r for r in remaining if filterFunction(el, r, error)] # Remaining elements that can replace el
        if(len(replacements) > 0):
            bestReplacement = max(replacements)

            improvement = bestReplacement - el
            improvedSum += improvement

            error = M - improvedSum

            improvedSol.remove(el)
            improvedSol += [bestReplacement]

            remaining.remove(bestReplacement)

    return improvedSol, improvedSum


def read_instance(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

        S = list(map(int, lines[0].split()))
        print("Instance of S with " + str(len(S)) + " elements")
        
        M = lines[1].split()[0]
        M = int(M)   
        
        return S, M
    
def read_large_instances(file_name):
    with open(file_name, 'r') as file:
        
        out = []
        
        csv_file = csv.reader(file, delimiter= '\t')
        
        for line in csv_file:
            out.append(line)
        
    return out

def rgli(S, M, iterations):
    
    finalSol = []
    finalSum = 0
    
    for j in range(iterations):
        sol, sum, remaining = randomGreedy(instance, M) # Perform random Greedy selection

        improvedSol, improvedSum = localImprovement(sol, sum, remaining, M) # Perform local improvement

        if improvedSum > finalSum:
            finalSum = improvedSum
            finalSol = improvedSol

    finalSol.sort()
    
    return finalSum, finalSol

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python RGLI.py <instance_file> iterations")
        sys.exit(1)
    
    filename = sys.argv[1]
    iterations = int(sys.argv[2])
    
    instances = read_large_instances(filename)
    for i in range(len(instances)):
        instances[i] = [int(j) for j in instances[i]]
    
    M= [89, 133, 9872, 10825, 1033062, 1000706]
    #S, M = read_instance(filename)
    
    for i, instance in enumerate(instances):
        
        finalSol = []
        finalSum = 0
        
        t0 = time.time_ns()
        
        finalSum, _ = rgli(instance, M[i], iterations)
        
        t1 = time.time_ns()
        
        print("Final sum: ", str(finalSum))
        print('time: ', (t1-t0) * 10**-9)
    #print(finalSol)

