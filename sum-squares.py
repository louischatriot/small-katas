from math import isqrt
from time import time
from random import shuffle, randint, randrange


Nmax = 1001

squares = set(i * i for i in range(1, isqrt(2 * Nmax) + 1))
nexts = {p: [n for n in range(1, Nmax) if p + n in squares and p != n] for p in range(0, Nmax)}
nexts[None] = [n for n in range(1, Nmax)]
pairs = set((a, b) for a in range(0, Nmax) for b in range(0, Nmax) if a + b in squares)

print("READY")


# for p in nexts:
    # shuffle(nexts[p])


the_list = []

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
                # the_list.append(res)
                print(res)
                # return res




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



# Returns all results we can get with an insertion
def insert(base, new):
    N = len(base)
    res = []

    if (base[0], new) in pairs:
        res.append([new] + [b for b in base])

    if (base[-1], new) in pairs:
        res.append([b for b in base] + [new])

    for i in range(0, N-1):
        if (base[i], new) in pairs and (base[i+1], new) in pairs:
            res.append(base[0:i+1] + [new] + base[i+1:])

    for i in range(0, N-1):
        if (base[i], new) not in pairs:
            continue

        for j in range(i+1, N):   # Technically could try starting with i+2 given the above
            if (base[j], new) not in pairs:
                continue

            # This case should not exist given the above
            if j == N-1:
                res.append(base[0:i+1] + [new] + list(reversed(base[i+1:])))
                continue

            if (base[i+1], base[j+1]) in pairs:
                res.append(base[0:i+1] + [new] + list(reversed(base[i+1:j+1])) + base[j+1:])
                continue



    return res


def insert_all(bases, new):
    res = []
    for base in bases:
        res += insert(base, new)
    return res


res_25 = [
    [2, 23, 13, 12, 24, 25, 11, 14, 22, 3, 1, 8, 17, 19, 6, 10, 15, 21, 4, 5, 20, 16, 9, 7, 18],
    [3, 22, 14, 2, 23, 13, 12, 4, 21, 15, 10, 6, 19, 17, 8, 1, 24, 25, 11, 5, 20, 16, 9, 7, 18],
    [4, 21, 15, 10, 6, 19, 17, 8, 1, 3, 22, 14, 2, 23, 13, 12, 24, 25, 11, 5, 20, 16, 9, 7, 18],
    [8, 17, 19, 6, 10, 15, 21, 4, 12, 13, 23, 2, 14, 22, 3, 1, 24, 25, 11, 5, 20, 16, 9, 7, 18],
    [9, 16, 20, 5, 4, 21, 15, 10, 6, 19, 17, 8, 1, 3, 22, 14, 11, 25, 24, 12, 13, 23, 2, 7, 18],
    [10, 15, 21, 4, 12, 13, 23, 2, 14, 22, 3, 6, 19, 17, 8, 1, 24, 25, 11, 5, 20, 16, 9, 7, 18],
    [11, 25, 24, 12, 13, 23, 2, 14, 22, 3, 1, 8, 17, 19, 6, 10, 15, 21, 4, 5, 20, 16, 9, 7, 18],
    [13, 23, 2, 14, 22, 3, 1, 8, 17, 19, 6, 10, 15, 21, 4, 12, 24, 25, 11, 5, 20, 16, 9, 7, 18],
    [18, 7, 2, 23, 13, 12, 24, 25, 11, 14, 22, 3, 1, 8, 17, 19, 6, 10, 15, 21, 4, 5, 20, 16, 9],
    [18, 7, 9, 16, 20, 5, 4, 21, 15, 10, 6, 19, 17, 8, 1, 3, 22, 14, 2, 23, 13, 12, 24, 25, 11],
    [18, 7, 9, 16, 20, 5, 4, 21, 15, 10, 6, 19, 17, 8, 1, 3, 22, 14, 11, 25, 24, 12, 13, 23, 2],
    [18, 7, 9, 16, 20, 5, 11, 25, 24, 1, 3, 22, 14, 2, 23, 13, 12, 4, 21, 15, 10, 6, 19, 17, 8],
    [18, 7, 9, 16, 20, 5, 11, 25, 24, 1, 8, 17, 19, 6, 3, 22, 14, 2, 23, 13, 12, 4, 21, 15, 10],
    [18, 7, 9, 16, 20, 5, 11, 25, 24, 1, 8, 17, 19, 6, 10, 15, 21, 4, 12, 13, 3, 22, 14, 2, 23],
    [18, 7, 9, 16, 20, 5, 11, 25, 24, 1, 8, 17, 19, 6, 10, 15, 21, 4, 12, 13, 23, 2, 14, 22, 3],
    [18, 7, 9, 16, 20, 5, 11, 25, 24, 12, 4, 21, 15, 10, 6, 19, 17, 8, 1, 3, 13, 23, 2, 14, 22],
    [18, 7, 9, 16, 20, 5, 11, 25, 24, 12, 4, 21, 15, 10, 6, 19, 17, 8, 1, 3, 22, 14, 2, 23, 13],
    [18, 7, 9, 16, 20, 5, 11, 25, 24, 12, 13, 23, 2, 14, 22, 3, 1, 8, 17, 19, 6, 10, 15, 21, 4],
    [22, 14, 2, 23, 13, 3, 1, 8, 17, 19, 6, 10, 15, 21, 4, 12, 24, 25, 11, 5, 20, 16, 9, 7, 18],
    [23, 2, 14, 22, 3, 13, 12, 4, 21, 15, 10, 6, 19, 17, 8, 1, 24, 25, 11, 5, 20, 16, 9, 7, 18]
]


res_30 = [
    [1, 24, 25, 11, 5, 4, 12, 13, 3, 6, 30, 19, 17, 8, 28, 21, 15, 10, 26, 23, 2, 14, 22, 27, 9, 16, 20, 29, 7, 18],
    [3, 13, 12, 4, 5, 11, 25, 24, 1, 15, 21, 28, 8, 17, 19, 30, 6, 10, 26, 23, 2, 14, 22, 27, 9, 16, 20, 29, 7, 18],
    [4, 5, 11, 25, 24, 12, 13, 3, 1, 15, 21, 28, 8, 17, 19, 30, 6, 10, 26, 23, 2, 14, 22, 27, 9, 16, 20, 29, 7, 18],
    [6, 30, 19, 17, 8, 28, 21, 4, 5, 11, 25, 24, 12, 13, 3, 1, 15, 10, 26, 23, 2, 14, 22, 27, 9, 16, 20, 29, 7, 18],
    [12, 13, 3, 6, 30, 19, 17, 8, 28, 21, 4, 5, 11, 25, 24, 1, 15, 10, 26, 23, 2, 14, 22, 27, 9, 16, 20, 29, 7, 18],
    [13, 12, 4, 5, 11, 25, 24, 1, 3, 6, 30, 19, 17, 8, 28, 21, 15, 10, 26, 23, 2, 14, 22, 27, 9, 16, 20, 29, 7, 18],
    [13, 12, 24, 25, 11, 5, 4, 21, 28, 8, 17, 19, 30, 6, 3, 1, 15, 10, 26, 23, 2, 14, 22, 27, 9, 16, 20, 29, 7, 18],
    [14, 2, 23, 26, 10, 6, 30, 19, 17, 8, 28, 21, 15, 1, 24, 25, 11, 5, 4, 12, 13, 3, 22, 27, 9, 16, 20, 29, 7, 18],
    [15, 1, 3, 13, 12, 24, 25, 11, 5, 4, 21, 28, 8, 17, 19, 30, 6, 10, 26, 23, 2, 14, 22, 27, 9, 16, 20, 29, 7, 18],
    [17, 19, 30, 6, 3, 13, 12, 4, 5, 11, 25, 24, 1, 8, 28, 21, 15, 10, 26, 23, 2, 14, 22, 27, 9, 16, 20, 29, 7, 18],
    [17, 19, 30, 6, 3, 13, 12, 24, 25, 11, 5, 4, 21, 28, 8, 1, 15, 10, 26, 23, 2, 14, 22, 27, 9, 16, 20, 29, 7, 18],
    [18, 7, 29, 20, 16, 9, 27, 22, 3, 13, 12, 4, 5, 11, 14, 2, 23, 26, 10, 6, 30, 19, 17, 8, 28, 21, 15, 1, 24, 25],
    [18, 7, 29, 20, 16, 9, 27, 22, 3, 13, 12, 4, 5, 11, 25, 24, 1, 15, 21, 28, 8, 17, 19, 30, 6, 10, 26, 23, 2, 14],
    [18, 7, 29, 20, 16, 9, 27, 22, 14, 2, 23, 13, 12, 4, 5, 11, 25, 24, 1, 3, 6, 30, 19, 17, 8, 28, 21, 15, 10, 26],
    [18, 7, 29, 20, 16, 9, 27, 22, 14, 2, 23, 13, 12, 24, 25, 11, 5, 4, 21, 28, 8, 17, 19, 30, 6, 3, 1, 15, 10, 26],
    [18, 7, 29, 20, 16, 9, 27, 22, 14, 2, 23, 26, 10, 6, 3, 13, 12, 4, 5, 11, 25, 24, 1, 15, 21, 28, 8, 17, 19, 30],
    [18, 7, 29, 20, 16, 9, 27, 22, 14, 2, 23, 26, 10, 6, 30, 19, 17, 8, 28, 21, 4, 5, 11, 25, 24, 12, 13, 3, 1, 15],
    [18, 7, 29, 20, 16, 9, 27, 22, 14, 2, 23, 26, 10, 6, 30, 19, 17, 8, 28, 21, 15, 1, 3, 13, 12, 4, 5, 11, 25, 24],
    [18, 7, 29, 20, 16, 9, 27, 22, 14, 2, 23, 26, 10, 6, 30, 19, 17, 8, 28, 21, 15, 1, 3, 13, 12, 24, 25, 11, 5, 4],
    [18, 7, 29, 20, 16, 9, 27, 22, 14, 2, 23, 26, 10, 6, 30, 19, 17, 8, 28, 21, 15, 1, 24, 25, 11, 5, 4, 12, 13, 3],
    [18, 7, 29, 20, 16, 9, 27, 22, 14, 2, 23, 26, 10, 15, 1, 3, 6, 30, 19, 17, 8, 28, 21, 4, 5, 11, 25, 24, 12, 13],
    [18, 7, 29, 20, 16, 9, 27, 22, 14, 2, 23, 26, 10, 15, 1, 3, 13, 12, 24, 25, 11, 5, 4, 21, 28, 8, 17, 19, 6, 30],
    [18, 7, 29, 20, 16, 9, 27, 22, 14, 2, 23, 26, 10, 15, 1, 3, 13, 12, 24, 25, 11, 5, 4, 21, 28, 8, 17, 19, 30, 6],
    [18, 7, 29, 20, 16, 9, 27, 22, 14, 2, 23, 26, 10, 15, 1, 8, 17, 19, 30, 6, 3, 13, 12, 24, 25, 11, 5, 4, 21, 28],
    [18, 7, 29, 20, 16, 9, 27, 22, 14, 2, 23, 26, 10, 15, 1, 8, 28, 21, 4, 5, 11, 25, 24, 12, 13, 3, 6, 30, 19, 17],
    [18, 7, 29, 20, 16, 9, 27, 22, 14, 2, 23, 26, 10, 15, 1, 24, 12, 13, 3, 6, 30, 19, 17, 8, 28, 21, 4, 5, 11, 25],
    [18, 7, 29, 20, 16, 9, 27, 22, 14, 2, 23, 26, 10, 15, 1, 24, 25, 11, 5, 4, 12, 13, 3, 6, 30, 19, 17, 8, 28, 21],
    [18, 7, 29, 20, 16, 9, 27, 22, 14, 2, 23, 26, 10, 15, 1, 24, 25, 11, 5, 4, 21, 28, 8, 17, 19, 30, 6, 3, 13, 12],
    [18, 7, 29, 20, 16, 9, 27, 22, 14, 2, 23, 26, 10, 15, 21, 28, 8, 1, 24, 25, 11, 5, 4, 12, 13, 3, 6, 30, 19, 17],
    [18, 7, 29, 20, 16, 9, 27, 22, 14, 2, 23, 26, 10, 15, 21, 28, 8, 17, 19, 30, 6, 3, 1, 24, 25, 11, 5, 4, 12, 13],
    [18, 7, 29, 20, 16, 9, 27, 22, 14, 2, 23, 26, 10, 15, 21, 28, 8, 17, 19, 30, 6, 3, 13, 12, 4, 5, 11, 25, 24, 1],
    [21, 28, 8, 17, 19, 30, 6, 3, 13, 12, 4, 5, 11, 25, 24, 1, 15, 10, 26, 23, 2, 14, 22, 27, 9, 16, 20, 29, 7, 18],
    [24, 25, 11, 5, 4, 12, 13, 3, 1, 15, 21, 28, 8, 17, 19, 30, 6, 10, 26, 23, 2, 14, 22, 27, 9, 16, 20, 29, 7, 18],
    [25, 11, 5, 4, 21, 28, 8, 17, 19, 30, 6, 3, 13, 12, 24, 1, 15, 10, 26, 23, 2, 14, 22, 27, 9, 16, 20, 29, 7, 18],
    [25, 24, 1, 15, 21, 28, 8, 17, 19, 30, 6, 10, 26, 23, 2, 14, 11, 5, 4, 12, 13, 3, 22, 27, 9, 16, 20, 29, 7, 18],
    [26, 10, 15, 1, 3, 6, 30, 19, 17, 8, 28, 21, 4, 5, 11, 25, 24, 12, 13, 23, 2, 14, 22, 27, 9, 16, 20, 29, 7, 18],
    [26, 10, 15, 21, 28, 8, 17, 19, 30, 6, 3, 1, 24, 25, 11, 5, 4, 12, 13, 23, 2, 14, 22, 27, 9, 16, 20, 29, 7, 18],
    [28, 21, 4, 5, 11, 25, 24, 12, 13, 3, 6, 30, 19, 17, 8, 1, 15, 10, 26, 23, 2, 14, 22, 27, 9, 16, 20, 29, 7, 18],
    [30, 6, 19, 17, 8, 28, 21, 4, 5, 11, 25, 24, 12, 13, 3, 1, 15, 10, 26, 23, 2, 14, 22, 27, 9, 16, 20, 29, 7, 18],
    [30, 19, 17, 8, 28, 21, 15, 1, 24, 25, 11, 5, 4, 12, 13, 3, 6, 10, 26, 23, 2, 14, 22, 27, 9, 16, 20, 29, 7, 18]

]


# Get one element at random in list
def pick(l):
    return l[randrange(0, len(l))]

# Swap i and j, reversing the list between them (included)
def super_swap(l, i, j):
    return l[0:i] + list(reversed(l[i:j+1])) + l[j+1:]




# base = [21, 28, 8, 17, 19, 30, 6, 3, 13, 12, 4, 5, 11, 25, 24, 1, 15, 10, 26, 23, 2, 14, 22, 27, 9, 16, 20, 29, 7, 18]

# for i in range(0, 30):
    # for j in range(0, 30):
        # if abs(i - j) > 1:
            # print(i, j)

# 1/0




# Ntest = 30
# t = res_30
# for i in range(1, 5):
    # t = insert_all(t, Ntest + i)
    # print(len(t))


# print(t[1])



base = [32, 17, 19, 30, 34, 15, 21, 28, 8, 1, 24, 25, 11, 5, 4, 12, 13, 3, 6, 10, 26, 23, 2, 14, 22, 27, 9, 16, 33, 31, 18, 7, 29, 20]


def get_next(base):
    N = len(base)
    new = N+1



    # NEED TO REALLY CODE INSERTION
    base.insert(10, new)
    base = super_swap(base, 11, 24)


    N = len(base)

    # Conflict
    c = 24
    if (base[c], base[c+1]) in pairs:
        1/0


    while True:
        # print("======================================")
        # print(base)
        # print("CONFLICT L", c, base[c])
        # print("CONFLICT R", c+1, base[c+1])

        if c+1 != 0 and (base[0], base[c+1]) in pairs:
            res = super_swap(base, 0, c)
            return res

        if c != N-1 and (base[c], base[N-1]) in pairs:
            res = super_swap(base, c+1, N-1)
            return res

        pos = []

        # Checking right of conflict
        for i in range(c+2, N-1):
            # print(i, base[i])
            if (base[c], base[i]) in pairs:
                # print("BOOM", i, base[i])
                if (base[c+1], base[i+1]) in pairs:
                    res = super_swap(base, c+1, i)
                    return res
                else:
                    pos.append((c+1, i, i))

        # Checking left of conflict
        for i in range(1, c):
            if (base[c+1], base[i]) in pairs:
                if (base[c], base[i-1]) in pairs:
                    res = super_swap(base, i-1, c)
                    return res
                else:
                    pos.append((i, c, i-1))

        # print(pos)

        s, e, c = pick(pos)
        # s, e, c = pos[0]

        # print("CHOSEN", s, e, c)

        base = super_swap(base, s, e)







res = get_next(base)
print("=============================================")
print("=============================================")
print("=============================================")

print(res)

# for i in range(1, len(res)):
    # print(res[i-1]+res[i])



def check(l):
    N = len(l)
    if any([(l[i-1], l[i]) not in pairs for i in range(1, N)]):
        raise ValueError("Not summing to a square")
    ll = sorted(l)
    if ll[0] != 1:
        raise ValueError("Minimum should be 1")
    if any([ll[i] - ll[i-1] != 1 for i in range(1, N)]):
        raise ValueError("Should contain all numbers up to length")

    return True

check(res)

1/0



def rand_method(N):
    l = [i for i in range(1, N+1)]
    shuffle(l)

    # l = [1, 3, 6, 19, 30, 34, 2, 23, 13, 36, 28, 8, 17, 32, 4, 21, 15, 10, 26, 38, 11, 25, 24, 12, 37, 27, 22, 14, 35, 29, 20, 5, 31, 18, 7, 9, 16, 33]

    base = [1, 3, 13, 36, 28, 8, 17, 32, 4, 21, 15, 34, 30, 19, 6, 10, 26, 23, 2, 7, 18, 31, 33, 16, 9, 27, 22, 14, 35, 29, 20, 5, 11, 25, 24, 12, 37]

    for i in range(1, 38):
        if (i, 38) in pairs:
            print(i, 38)

    1/0

    # l = [i for i in base]
    # idx = randrange(0, 37)
    # l.insert(idx, 38)


    # Fixing for now
    # idx = 4
    # l = [1, 3, 13, 36, 38, 28, 8, 17, 32, 4, 21, 15, 34, 30, 19, 6, 10, 26, 23, 2, 7, 18, 31, 33, 16, 9, 27, 22, 14, 35, 29, 20, 5, 11, 25, 24, 12, 37]

    # print(idx)
    # print(l)

    t = randrange(0,36)
    base[t], base[t+1] = base[t+1], base[t]



    for i in range(0, N-2):
        # if i == idx -1 or i == idx:
            # continue

        if (l[i], N) in pairs and (N, l[i+1]) in pairs:
            print(i)


    1/0


    # ok = all((l[i-1], l[i]) in pairs for i in range(1, N))

    nbad = sum([1 if (l[i-1], l[i]) not in pairs else 0 for i in range(1, N)])
    print(nbad)
    1/0


    while True:
        nbad = sum([1 if (l[i-1], l[i]) not in pairs else 0 for i in range(1, N)])
        # print("---")

        for i in range(0, N-1):
            if (l[i], l[i+1]) not in pairs:

                for j in range(N-1, i+1, -1):
                    if (l[j-1], l[j]) not in pairs:
                        # if (l[j], l[i+1]) in pairs and (l[j-1], l[i]) in pairs:
                        if (l[j], l[i+1]) in pairs:
                            l[i], l[j] = l[j], l[i]
                            break

        ok = all((l[i-1], l[i]) in pairs for i in range(1, N))
        if ok:
            break

        nbad_after = sum([1 if (l[i-1], l[i]) not in pairs else 0 for i in range(1, N)])
        print(nbad_after)
        if nbad_after == nbad:
            print("Reshuffle")
            shuffle(l)
        # print(nbad)

        # 1/0

    print(ok)


def square_sums(n):
    return launch_dfs(n)





start = time()

res = launch_dfs(30)
# res = rand_method(38)

print(res)

print("===>", time() - start)


# for l in the_list:
    # ss = [l[i-1]+l[i] for i in range(1, len(l))]
    # print(ss)




