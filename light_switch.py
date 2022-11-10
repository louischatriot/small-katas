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









logging = True

def log(s):
    if logging:
        print(s)


def print_matrix(m):
    res = '\n'.join([' '.join(map(str, l)) for l in m])
    log(res)

M = 15
digit_sum = [sum(1 if d == '1' else 0 for d in bin(i)) % 2 for i in range(0, 2**M - 1)]


def get_switch_matrix(n, switches):
    m = len(switches)

    switches_a = [[0 for j in range(0, m)] for i in range(0, n)]
    for j, s in enumerate(switches):
        for i in s:
            switches_a[i][j] = 1

    return switches_a


def solve_brute(n, switches):
    m = len(switches)
    bins = [sum(0 if d == 0 else 2 ** i for i, d in enumerate(reversed(l))) for l in get_switch_matrix(n, switches)]

    for test in range(0, 2**m - 1):
        if all(digit_sum[b & test] == 1 for b in bins):
            return True


# If light i is entirely determined by pos, return True
# If it is determined to be not compatible, return False
# If only one switch is needed to make it right, return the switch and position => not for now, future optimization
# If we can't tell, return None
def check_i(switches_a, i, pos):
    for j in range(0, len(pos)):
        res = 0
        if switches_a[i][j] == 1:
            if pos[j] == 2:
                return None   # Can't tell yet
            else:
                res += pos[j]

    return res % 2 == 1



def propagate(switches_a, pos, idx):
    n = len(switches_a)
    m = len(pos)

    for i in range(0, n):
        # Switch we are testing has impact on this light
        if switches_a[i][idx] == 1:
            if check_i(switches_a, i, pos) is False:
                return False

    return pos   # No true propagation for now, future optimization


def dfs(switches_a, pos, idx = 0):
    n = len(switches_a)
    m = len(pos)


    if idx == m - 1:
        return propagate(switches_a, pos, m - 1) is not False

    if pos[idx] != 2:
        return dfs(switches_a, pos, idx + 1)

    for p in [0, 1]:
        # Can be optimized to avoid copying twice
        _pos = [d for d in pos]
        _pos[idx] = p

        _pos = propagate(switches_a, _pos, idx)
        if _pos:
            if dfs(switches_a, _pos, idx + 1):
                return True

    return False


def light_switch(n, switches):
    m = len(switches)

    if m < n:
        return solve_brute(n, switches)

    switches_a = get_switch_matrix(n, switches)
    pos = [1 for i in range(0, n)]

    print_matrix(switches_a)

    for i0 in range(0, n):
        # Making sure we have a 1 at the beginning of the diagonal
        # TODO: what bout when we don't find a line with a 1
        if switches_a[i0][i0] != 1:
            for ig in range(i0+1, n):
                if switches_a[ig][i0] == 1:
                    swp = switches_a[i0]
                    switches_a[i0] = switches_a[ig]
                    switches_a[ig] = swp

                    pos[ig], pos[i0] = pos[i0], pos[ig]
                    break


        # Remove ones in the column
        for i in range(0, n):
            if i != i0:
                if switches_a[i][i0] == 1:
                    switches_a[i] = [(switches_a[i][j] + switches_a[i0][j]) % 2 for j in range(0, m)]
                    pos[i] = (pos[i] + pos[i0]) % 2



    print("========================================")
    print("========================================")
    print_matrix(switches_a)

    print(' '.join(map(str, pos)))


    pos = pos + [0 for i in range(n, m)]

    print(pos)

    print(len(pos))
    print(m)

    switches_a = get_switch_matrix(n, switches)

    print("%%%%%%%%%%%%%%%%%")
    for i in range(0, n):
        res = sum(pos[j] * switches_a[i][j] for j in range(0, m))
        print(res % 2)




# n = 31
# switches = [
    # [0, 2, 4, 5, 6, 9, 10],
    # [1, 3, 5, 6, 7, 8, 11],
    # [1, 2, 3, 4, 6, 7, 8, 11],
    # [2, 4, 9],
    # [7, 8, 9, 10],
    # [1, 4, 8, 11],
    # [6, 9],
    # [8, 9, 10],
    # [2, 3, 5, 7, 10, 11],
    # [x for x in range(12, 31)],
    # [x for x in range(12, 20)],
    # [x for x in range(21, 30)],
    # [x for x in range(4, 31)],
    # [x for x in range(6, 8)],
    # [x for x in range(17, 29)],
# ]




# Should be False
# n = 13
# switches = [[0, 1, 2, 3, 6, 7, 9], [1, 2, 3, 4, 5, 7, 10, 11, 12], [2, 4, 5, 6, 7, 8, 11, 12], [1, 4, 5, 7, 8], [0, 1, 2, 3, 4, 6, 7, 10, 12], [0, 1, 2, 3, 4, 9, 10, 11, 12], [1, 4, 5, 6, 8, 9, 11, 12], [1, 4, 5, 7, 8, 9, 10], [0, 1, 2, 7, 8, 9, 10, 11], [2, 3, 5, 6, 9, 10, 11, 12], [2, 3, 5, 6, 8, 9, 10, 11, 12], [1, 2, 4, 5, 8, 9, 10, 12], [1, 2, 3, 4, 5, 7, 8, 11, 12], [0, 2, 5, 6, 7, 8, 9, 10, 11, 12], [0, 1, 2, 4, 5, 9, 10, 11, 12]]



# Should be True
n = 12
switches = [[0, 1, 3, 4, 7, 8, 10, 11], [2, 3, 5, 6, 8, 10, 11], [0, 1, 4, 5, 6, 8, 9, 10], [0, 1, 3, 4, 6, 9, 10, 11], [1, 3, 5, 6, 9, 11], [3, 4, 5, 6, 7, 8, 9, 11], [0, 2, 5, 6, 7, 8, 9, 10, 11], [0, 1, 4, 5, 9, 10, 11], [0, 3, 4, 5, 6, 8, 9, 11], [0, 1, 2, 4, 6, 8, 9, 10, 11], [1, 2, 3, 6, 8, 9, 10, 11], [0, 1, 3, 4, 6, 8, 9, 10, 11], [2, 3, 4, 5, 6, 7, 9, 10, 11], [0, 1, 4, 5, 6, 9, 11], [0, 1, 3, 6, 7, 9, 11], [0, 1, 2, 3, 4, 8, 9, 11], [3, 4, 5, 7, 8, 9, 10, 11], [2, 3, 4, 5, 8, 9], [0, 1, 2, 3, 4, 6, 8], [0, 2, 5, 6, 7, 10, 11], [0, 1, 2, 3, 5, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 11], [0, 1, 2, 3, 4, 6, 7, 9, 11], [0, 2, 3, 4, 7, 8, 9], [1, 3, 5, 6, 7, 8, 9, 10], [0, 3, 5, 7, 8, 9, 10], [1, 3, 4, 6, 8, 9, 10, 11], [3, 6, 7, 8, 9, 11]]



print_matrix(switches)
print(len(switches))


t.reset()


NN = 1
for i in range(0, NN):
    res = light_switch(n, switches)

t.time("Done")

print(res)



