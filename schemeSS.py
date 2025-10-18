import sys

def merge_lists(L, L_plus):
    merged = []
    i, j = 0, 0
    while i < len(L) and j < len(L_plus):
        if L[i][0] < L_plus[j][0]:
            merged.append(L[i]); i += 1
        else:
            merged.append(L_plus[j]); j += 1
    merged.extend(L[i:])
    merged.extend(L_plus[j:])
    return merged

def trim(L, delta):
    trimmed = [L[0]]
    last_val = L[0][0]
    for val, chosen in L[1:]:
        if val > last_val * (1 + delta):
            trimmed.append((val, chosen))
            last_val = val
    return trimmed

def remove_greater(L, M):
    return [(val, chosen) for val, chosen in L if val <= M]

def schemeSS(S, M, eps):
    n = len(S)
    delta = eps / (2 * n)
    L = [(0, [False] * n)]
    
    for i, xi in enumerate(S):
        L_plus = []
        for val, chosen in L:
            new_chosen = chosen.copy()
            new_chosen[i] = True
            L_plus.append((val + xi, new_chosen))
       
        L = merge_lists(sorted(L), sorted(L_plus))
        L = trim(L, delta)
        L = remove_greater(L, M)
    
    best_val, best_chosen = L[-1]
    subset = [S[i] for i, used in enumerate(best_chosen) if used]
    return best_val, subset


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
