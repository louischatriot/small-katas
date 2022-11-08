import time
class Timer():
    def __init__(self):
        self.reset()

    def reset(self):
        self.start = time.time()

    def time(self, message = ''):
        duration = time.time() - self.start
        print(f"{message} ===> Duration: {duration}")
        self.reset()

t = Timer()







import numpy as np


logging = True

def log(s):
    if logging:
        print(s)


def print_matrix(m):
    res = '\n'.join([' '.join(map(str, l)) for l in m])
    log(res)


def solve_brute(n, switches):
    m = len(switches)
    digit_sum = [sum(1 if d == '1' else 0 for d in bin(i)) for i in range(0, 2**m - 1)]

    return True

    # switches_a = [[1 if i in s else 0 for s in switches] for i in range(0, n)]

    switches_a = [[0 for j in range(0, m)] for i in range(0, n)]
    for j, s in enumerate(switches):
        for i in s:
            switches_a[i][j] = 1


    bins = [sum(0 if d == 0 else 2 ** i for i, d in enumerate(reversed(l))) for l in switches_a]

    for b in bins:
        log(bin(b))

    print_matrix(switches_a)


    all_on = [1 for i in range(0, m)]

    all_on_b = int('1' * m, 2)


    all_good = 2**m - 1

    print("=====================")
    print(bin(all_good))


    for b in bins:
        print("--------------------------------")
        print(bin(b))
        print(bin(b ^ all_good))


    for test in range(0, 2**m - 1):
        if all(b ^ test == all_good for b in bins):
            return bin(test)





def light_switch(n, switches):
    pass







n = 31
switches = [
    [0, 2, 4, 5, 6, 9, 10],
    [1, 3, 5, 6, 7, 8, 11],
    [1, 2, 3, 4, 6, 7, 8, 11],
    [2, 4, 9],
    [7, 8, 9, 10],
    [1, 4, 8, 11],
    [6, 9],
    [8, 9, 10],
    [2, 3, 5, 7, 10, 11],
    [x for x in range(12, 31)],
    [x for x in range(12, 20)],
    [x for x in range(21, 30)],
    [x for x in range(4, 31)],
    [x for x in range(6, 8)],
    [x for x in range(17, 29)],
]


print_matrix(switches)


t.reset()


NN = 10
for i in range(0, NN):
    res = solve_brute(n, switches)

t.time("Done")

log(res)



