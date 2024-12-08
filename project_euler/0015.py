import functools

@functools.cache
def lattice(n, m):
    if n == 0:
        return 1

    if m == 0:
        return 1

    return lattice(n, m-1) + lattice(n-1, m)


res = lattice(20, 20)
print(res)



