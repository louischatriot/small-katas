from time import time


def possibilities(clues, N):
    res = []

    if len(clues) == 0:
        return []

    if len(clues) == 1:
        c = clues[0]
        if c > N:
            return []
        for i in range(0, N-c+1):
            res.append([0] * i + [1] * c + [0] * (N-c-i))
        return res

    R = N - sum(clues[1:]) - (len(clues) - 2)
    c = clues[0]
    for r in range(c+1, R):
        heads = possibilities((c,), r)

        print(heads)
        print("============================")

        for h in heads:
            print("YO")
            print(N-r-1)
            for t in possibilities(clues[1:], N - r - 1):
                print("EEE")
                res.append(h + [0] + t)

    return res


class Nonogram:
    def __init__(self, clues):
        self.colclues = clues[0]
        self.rowclues = clues[1]
        self.N = len(self.rowclues)
        self.M = len(self.colclues)



    def solve(self):
        pass













res = possibilities((3,4,5), 20)

for r in res:
    print(r)




clues = (
    ((1, 1), (4,), (1, 1, 1), (3,), (1,)),
    ((1,), (2,), (3,), (2, 1), (4,))
)

ans = ((0, 0, 1, 0, 0),
       (1, 1, 0, 0, 0),
       (0, 1, 1, 1, 0),
       (1, 1, 0, 1, 0),
       (0, 1, 1, 1, 1))



start = time()

n = Nonogram(clues)



print("==> Duration:", time() - start)



