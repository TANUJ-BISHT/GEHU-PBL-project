# banker.py

def is_safe_state(allocation, max_matrix, available):
    n = len(allocation)       # number of processes
    m = len(available)        # number of resources

    # Step 1: Calculate Need matrix
    need = [[max_matrix[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]
    finish = [False] * n
    work = available[:]
    safe_sequence = []

    while len(safe_sequence) < n:
        found = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                # This process can run
                for j in range(m):
                    work[j] += allocation[i][j]
                finish[i] = True
                safe_sequence.append(i)
                found = True
                break
        if not found:
            return False, []  # No safe sequence found

    return True, safe_sequence
