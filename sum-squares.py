from math import isqrt
from time import time


Nmax = 1001

squares = set(i * i for i in range(1, isqrt(2 * Nmax) + 1))
nexts = {p: [n for n in range(1, Nmax) if p + n in squares and p != n] for p in range(0, Nmax)}
nexts[None] = [n for n in range(1, Nmax)]




def dfs(l, s, N):
    if len(l) >= N:
        return l

    for n in nexts[l[-1]]:
        if n not in s and n <= N:
            _l = [i for i in l]
            _s = {i for i in s}
            _l.append(n)
            _s.add(n)

            res = dfs(_l, _s, N)
            if res:
                return res




    return None


# To save a comparison ...
def launch_dfs(N):
    for n in nexts[None]:
        if n <= N:
            s = set()
            s.add(n)
            res = dfs([n], s, N)
            if res:
                return res

    return False

def square_sums(n):
    return launch_dfs(n)



start = time()

res = launch_dfs(2)

print(res)

print("===>", time() - start)
