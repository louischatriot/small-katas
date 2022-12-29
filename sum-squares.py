from math import isqrt
from time import time
from random import shuffle, randint, randrange


Nmax = 1301

squares = set(i * i for i in range(1, isqrt(2 * Nmax) + 1))
nexts = {p: [n for n in range(1, Nmax) if p + n in squares and p != n] for p in range(0, Nmax)}
nexts[None] = [n for n in range(1, Nmax)]
pairs = set((a, b) for a in range(0, Nmax) for b in range(0, Nmax) if a + b in squares)

print("READY")


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

# Get one element at random in list
def pick(l):
    return l[randrange(0, len(l))]

# Swap i and j, reversing the list between them (included)
def super_swap(l, i, j):
    return l[0:i] + list(reversed(l[i:j+1])) + l[j+1:]


base = [32, 17, 19, 30, 34, 15, 21, 28, 8, 1, 24, 25, 11, 5, 4, 12, 13, 3, 6, 10, 26, 23, 2, 14, 22, 27, 9, 16, 33, 31, 18, 7, 29, 20]


def get_next(base):
    N = len(base)
    new = N+1

    if (base[0], new) in pairs:
        return [new] + base

    if (base[-1], new) in pairs:
        return base + [new]

    pos = []
    for i in range(1, N-1):
        if (base[i], new) in pairs:
            if (base[i+1], new) in pairs:
                return base[0:i+1] + [new] + base[i+1:]
            else:
                pos.append(i)

    # c, c+1 is the conflict
    c = pick(pos) + 1
    base.insert(c, new)

    N = len(base)
    while True:
        if c+1 != 0 and (base[0], base[c+1]) in pairs:
            return super_swap(base, 0, c)

        if c != N-1 and (base[c], base[N-1]) in pairs:
            return super_swap(base, c+1, N-1)

        pos = []

        # Checking right of conflict
        for i in range(c+2, N-1):
            if (base[c], base[i]) in pairs:
                if (base[c+1], base[i+1]) in pairs:
                    return super_swap(base, c+1, i)
                else:
                    pos.append((c+1, i, i))

        # Checking left of conflict
        for i in range(1, c):
            if (base[c+1], base[i]) in pairs:
                if (base[c], base[i-1]) in pairs:
                    return super_swap(base, i, c)
                else:
                    pos.append((i, c, i-1))

        s, e, c = pick(pos)
        base = super_swap(base, s, e)


def check(l):
    N = len(l)

    for i in range(1, N):
        if (l[i-1], l[i]) not in pairs:
            raise ValueError(f"Not summing to a square: {i}")

    ll = sorted(l)
    if ll[0] != 1:
        raise ValueError("Minimum should be 1")
    if any([ll[i] - ll[i-1] != 1 for i in range(1, N)]):
        raise ValueError("Should contain all numbers up to length")

    return True



print("=============================================")
print("=============================================")
print("=============================================")


start = time()



base = [433, 243, 118, 323, 302, 139, 150, 426, 103, 153, 288, 241, 435, 6, 30, 51, 273, 211, 230, 395, 46, 278, 206, 155, 41, 215, 314, 262, 222, 178, 398, 331, 294, 282, 343, 186, 138, 346, 95, 161, 200, 284, 5, 31, 369, 360, 424, 417, 312, 172, 269, 356, 428, 413, 116, 208, 192, 132, 309, 220, 104, 425, 251, 110, 179, 305, 371, 70, 414, 27, 373, 252, 72, 49, 351, 325, 404, 380, 61, 300, 376, 408, 76, 365, 364, 212, 149, 292, 384, 400, 225, 304, 321, 355, 374, 67, 158, 283, 293, 383, 242, 199, 162, 367, 33, 48, 276, 13, 183, 217, 144, 385, 291, 334, 107, 14, 347, 229, 255, 69, 187, 174, 310, 419, 65, 259, 366, 34, 47, 353, 176, 148, 108, 88, 56, 113, 416, 368, 308, 53, 28, 141, 84, 316, 213, 12, 349, 180, 396, 280, 204, 85, 399, 330, 246, 379, 105, 219, 181, 15, 1, 80, 64, 297, 328, 348, 52, 432, 352, 177, 223, 101, 68, 221, 263, 362, 122, 74, 182, 218, 358, 318, 166, 3, 397, 279, 10, 90, 106, 423, 361, 315, 261, 415, 26, 170, 359, 370, 71, 290, 335, 194, 431, 298, 327, 249, 75, 121, 320, 164, 277, 299, 377, 407, 169, 120, 136, 188, 388, 341, 20, 124, 45, 36, 253, 372, 112, 57, 24, 337, 239, 50, 434, 350, 134, 307, 93, 163, 62, 422, 19, 342, 387, 238, 338, 191, 209, 115, 29, 260, 224, 32, 329, 247, 237, 339, 145, 296, 233, 23, 173, 83, 17, 272, 89, 311, 265, 411, 214, 227, 97, 99, 190, 210, 151, 333, 196, 245, 79, 405, 324, 117, 207, 322, 303, 226, 98, 386, 143, 82, 114, 111, 250, 326, 203, 22, 59, 137, 7, 393, 91, 165, 60, 301, 375, 154, 287, 37, 363, 78, 43, 38, 11, 313, 171, 270, 54, 430, 146, 254, 2, 142, 147, 429, 412, 264, 25, 119, 410, 266, 58, 86, 275, 401, 128, 16, 9, 391, 285, 244, 156, 168, 232, 129, 160, 96, 193, 336, 340, 389, 236, 205, 420, 421, 63, 18, 382, 102, 427, 357, 268, 216, 409, 267, 133, 228, 256, 185, 40, 81, 175, 21, 235, 126, 403, 381, 295, 234, 55, 345, 184, 257, 319, 306, 135, 189, 100, 125, 131, 94, 195, 289, 240, 201, 123, 73, 8, 392, 92, 77, 4, 140, 344, 281, 248, 152, 44, 317, 167, 157, 39, 42, 127, 197, 332, 109, 35, 406, 378, 198, 286, 390, 394, 231, 130, 354, 271, 258, 418, 66, 159, 202, 87, 274, 402]


res = get_next(base)
check(res)

for i in range(0, 800):
    # print(i)
    res = get_next(res)
    # check(res)

print("==> DURATION:", time() - start)


print(res)
check(res)

1/0





def square_sums(n):
    return launch_dfs(n)





start = time()

res = launch_dfs(30)

print(res)

print("===>", time() - start)






