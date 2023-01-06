from time import time
import numpy as np





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

        # print(heads)
        # print("============================")

        for h in heads:
            # print("YO")
            # print(N-r-1)
            for t in possibilities(clues[1:], N - r - 1):
                # print("EEE")
                res.append(h + [0] + t)

    return res


class Nonogram:
    def __init__(self, clues):
        self.colclues = clues[0]
        self.rowclues = clues[1]
        self.N = len(self.rowclues)
        self.M = len(self.colclues)
        self.grid = [['?' for _ in range(0, self.M)] for _ in range(0, self.N)]


    def print(self):
        print('\n'.join([' '.join(['O' if c == 1 else ('x' if c == 0 else '.') for c in l]) for l in self.grid]))
        print("========================================================")


    def print_clues(self):
        print("ROW CLUES:", self.rowclues)
        print("COL CLUES:", self.colclues)
        print("========================================================")


    def deduce_initial(self):
        N, M = self.N, self.M
        changed = set()

        # Cannot slide much
        # for x, clue in enumerate(self.rowclues):
            # movable = M - sum(clue) - (len(clue) - 1)

            # if movable == 0:
                # y = 0
                # for _ in range(0, clue[0]):
                    # self.grid[x][y] = 1
                    # y += 1

                # for c in clue[1:]:
                    # self.grid[x][y] = 0
                    # y += 1

                    # for _ in range(0, c):
                        # self.grid[x][y] = 1
                        # y += 1

            # else:
                # for i, c in enumerate(clue):
                    # if c > movable:
                        # before = sum(clue[0:i]) + len(clue[0:i])
                        # for dy in range(0, c - movable):
                            # self.grid[x][before + movable + dy] = 1


        # Cannot slide much
        for y, clue in enumerate(self.colclues):
            movable = N - sum(clue) - (len(clue) - 1)

            if movable == 0:
                x = 0
                for _ in range(0, clue[0]):
                    self.grid[x][y] = 1
                    x += 1

                for c in clue[1:]:
                    self.grid[x][y] = 0
                    x += 1

                    for _ in range(0, c):
                        self.grid[x][y] = 1
                        x += 1

            else:
                for i, c in enumerate(clue):
                    if c > movable:
                        before = sum(clue[0:i]) + len(clue[0:i])
                        for dx in range(0, c - movable):
                            self.grid[before + movable + dx][y] = 1

    def solve(self):
        pass













# res = possibilities((3,4,5), 20)

# for r in res:
    # print(r)




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

n.print_clues()
n.print()

n.deduce_initial()


n.print()




# res = possibilities((3,4,5,6,7), 41)

print("==> Duration:", time() - start)



