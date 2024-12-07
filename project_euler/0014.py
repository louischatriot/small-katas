mem = dict()  # Nice speed up from memoization

def collatz(n):
    if n == 1:
        return 1

    if n in mem:
        return mem[n]

    if n % 2 == 0:
        res = 1 + collatz(n // 2)
    else:
        res = 1 + collatz(3 * n + 1)

    mem[n] = res
    return res


N = 1000000
res = -1
best = -1


for n in range(1, N):
    c = collatz(n)
    if c > best:
        best = c
        res = n

    res = max(res, collatz(n))

print(res)


