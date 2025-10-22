'''Generates sets with random numbers up to a given value related to the set length and without repetitions (set)
   Given the desire set length, L, it creates a numpy array with integers from 1 to 2L. Then obtaines a 
   random sample with L elements, finally sorts the resulting set.
   
   @author: Andre Wemans, 48432
   @author: Pedro Lopes, 57514'''


#%% Imports
import numpy as np
import sys

#%% Functions
def generator(size):
	'''Generates a set with the given size with random numbers from 1 to 2 size without repetitions
	size: the set size to be generate
   
	out: numpy array with the set generated and sorted from lower to highr number'''

	#Generates the population of number form 1 to 2 size
	rng = np.random.default_rng()
	population = np.linspace(1, 4 * size, 2 * size, dtype= int)
	
	sample = rng.choice(population, size, replace= False)
	
	sample = np.sort(sample)
	
	return sample
#%% Program
if __name__ == '__main__':
    sizes = [10, 30, 50] #Sizes to generate sets
    
    #Opens file
    with open('sets.txt', 'w') as file:
        #for each size
        for size in sizes:
            #generates 3 sets
            for i in range(3):
                s = generator(size)
                #for each element in the numpy array write it to the file
                for j in range(s.size-1):
                    file.write(str(s[j]) + '\t')
                #writes the last element
                file.write(str(s[-1]) + '\n')