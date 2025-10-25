#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implements the schemeSS algorithm given in theorical class 03
for solving a maximum subset-sum problem using triming the solutuins
that are closer to a factor of each other

Receives a set of numbers, a value and the trimming factor 
and gives a approximation to the maximum sum of elements of a subset equal or 
less than the value

@author: Andre Wemans, 48432
@author: Pedro Lopes, 57514
"""
import sys
import time

def merge_lists(L, L_plus):
    merged = []
    i, j = 0, 0
    len_L, len_L_plus = len(L), len(L_plus)
    
    while i < len_L and j < len_L_plus:
        if L[i][0] < L_plus[j][0]:
            merged.append(L[i]); i += 1
        else:
            merged.append(L_plus[j]); j += 1
            
    if i < len_L:
        merged.extend(L[i:])
    
    if j < len_L_plus:
        merged.extend(L_plus[j:])
        
    return merged

def merge_lists_sol(L, L_plus):
    merged = []
    i, j = 0, 0
    len_L, len_L_plus = len(L), len(L_plus)
    
    while i < len_L and j < len_L_plus:
        if L[i] < L_plus[j]:
            merged.append(L[i]); i += 1
        else:
            merged.append(L_plus[j]); j += 1
            
    if i < len_L:
        merged.extend(L[i:])
    
    if j < len_L_plus:
        merged.extend(L_plus[j:])
        
    return merged

def trim(L, delta):
    
    trimmed = [L[0]]
    last_val = L[0][0]
    threshold_multiplier = 1 + delta
    
    for item in L[1:]:
        val = item[0]
        if val > last_val * threshold_multiplier:
            trimmed.append(item)
            last_val = val
    
    return trimmed

def trim_sol(L, delta):
    
    trimmed = [L[0]]
    last_val = L[0]
    threshold_multiplier = 1 + delta
    
    for item in L[1:]:
        val = item
        if val > last_val * threshold_multiplier:
            trimmed.append(item)
            last_val = val
    
    return trimmed

def remove_greater(L, M):
    # Since L is sorted, find the last element <= M
    left, right = 0, len(L) - 1
    result_idx = 0
    
    while left <= right:
        mid = (left + right) // 2
        if L[mid][0] <= M:
            result_idx = mid
            left = mid + 1
        else:
            right = mid - 1
    
    return L[:result_idx + 1]

def remove_greater_sol(L, M):
    # Since L is sorted, find the last element <= M
    left, right = 0, len(L) - 1
    result_idx = 0
    
    while left <= right:
        mid = (left + right) // 2
        if L[mid] <= M:
            result_idx = mid
            left = mid + 1
        else:
            right = mid - 1
    
    return L[:result_idx + 1]

def schemeSS(S, M, eps):
    n = len(S)
    delta = eps / (2 * n)
    
    L = [(0, ())]
    
    for i, xi in enumerate(S):
        # Create L_plus
        L_plus = [(val + xi, indices + (i,)) for val, indices in L]
        
        # Merge (both already sorted)
        L = merge_lists(L, L_plus)
        
        # Trim
        L = trim(L, delta)
        
        # Remove elements > M
        L = remove_greater(L, M)
    
    # Extract best solution
    best_val, best_indices = L[-1]
    subset = [S[i] for i in best_indices]
    
    return best_val, subset

def schemeSS_val(S, M, eps):
    n = len(S)
    delta = eps / (2 * n)
    
    L = [0]
    
    for i, xi in enumerate(S):
        # Create L_plus
        L_plus = [val + xi for val in L]
        
        # Merge (both already sorted)
        L = merge_lists_sol(L, L_plus)
        
        # Trim
        L = trim_sol(L, delta)
        
        # Remove elements > M
        L = remove_greater_sol(L, M)

    # Extract best solution value
    best_val = L[-1]
    
    return best_val

def schemeSS_val_timed(S, M, eps):
    
    t0 = time.time_ns()
    
    n = len(S)
    delta = eps / (2 * n)
    
    L = [0]
    
    for i, xi in enumerate(S):
        # Create L_plus
        L_plus = [val + xi for val in L]
        
        # Merge (both already sorted)
        L = merge_lists_sol(L, L_plus)
        
        # Trim
        L = trim_sol(L, delta)
        
        # Remove elements > M
        L = remove_greater_sol(L, M)

    # Extract best solution value
    best_val = L[-1]
    
    t1 = time.time_ns()
    
    return (t1 - t0) / 10**9, best_val


def read_instance(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

        S = list(map(int, lines[0].split()))
        print("Instance of S with " + str(len(S)) + " elements")
        
        M, eps = lines[1].split()
        M, eps = int(M), float(eps)    
        
        return S, M, eps

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python schemeSS.py <instance_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    S, M, eps = read_instance(filename)
    best_val, subset = schemeSS(S, M, eps)
    print("Best value:", best_val)
    print("Subset:", subset)
