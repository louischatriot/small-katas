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



def print_matrix(m):
    res = '\n'.join([' '.join(map(str, l)) for l in m])
    print(res)


def solve_brute(n, switches):
    m = len(switches)

    switches_a = [[1 if i in s else 0 for s in switches] for i in range(0, n)]

    print_matrix(switches_a)

    all_on = [1 for i in range(0, m)]

    res = np.matmul(switches_a, all_on)

    print(res)

    res = [i % 2 for i in res]

    print(res)

    print(len(res))




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


solve_brute(n, switches)


