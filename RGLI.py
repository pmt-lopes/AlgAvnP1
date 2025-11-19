import sys
import random

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
    
    for el in sol:
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

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python RGLI.py <instance_file> iterations")
        sys.exit(1)
    
    filename = sys.argv[1]
    iterations = int(sys.argv[2])
    S, M = read_instance(filename)

    finalSol = []
    finalSum = 0

    for i in range(iterations):
        sol, sum, remaining = randomGreedy(S, M) # Perform random Greedy selection

        improvedSol, improvedSum = localImprovement(sol, sum, remaining, M) # Perform local improvement

        if improvedSum > finalSum:
            finalSum = improvedSum
            finalSol = improvedSol

    finalSol.sort()
    print("Final sum: ", str(finalSum))
    print(finalSol)

