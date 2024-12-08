import itertools

n = 0
for l in itertools.permutations([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]):
    n += 1
    if n == 1000000:
        print(''.join(map(str, l)))
        1/0
