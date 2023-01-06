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



def get_rows_and_cols(changed):
    rows = set()
    cols = set()

    for x, y in changed:
        rows.add(x)
        cols.add(y)

    return (rows, cols)


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


    def set(self, x, y, value, changed, transpose = False):
        if transpose:
            x, y = y, x

        if value != self.grid[x][y]:
            if self.grid[x][y] == '?':
                self.grid[x][y] = value
                changed.add((x, y))
            else:
                # Should handle with a return
                raise ValueError("Wrong guess earlier")


    def get(self, x, y, transpose = False):
        if transpose:
            x, y = y, x

        return self.grid[x][y]


    def deduce_initial(self):
        changed = set()   # Should really keep track of lines and columns separately but easier to debug

        # Cannot slide much
        for clues, transpose, M in [(self.rowclues, False, self.M), (self.colclues, True, self.N)]:
            for x, clue in enumerate(clues):
                movable = M - sum(clue) - (len(clue) - 1)

                if movable == 0:
                    y = 0
                    for _ in range(0, clue[0]):
                        self.set(x, y, 1, changed, transpose)
                        y += 1

                    for c in clue[1:]:
                        self.set(x, y, 0, changed, transpose)
                        y += 1

                        for _ in range(0, c):
                            self.set(x, y, 1, changed, transpose)
                            y += 1

                else:
                    for i, c in enumerate(clue):
                        if c > movable:
                            before = sum(clue[0:i]) + len(clue[0:i])
                            for dy in range(0, c - movable):
                                self.set(x, before + movable + dy, 1, changed, transpose)

        return changed


    def deduce(self, changed):
        rows, cols = get_rows_and_cols(changed)

        print(rows)
        print(cols)

        changed = set()

        # When one filled square is close to a border
        # Only case handled for now = glued to a border
        for clues, transpose, the_rows, M in [(self.rowclues, False, rows, self.M), (self.colclues, True, cols, self.N)]:
            for x in the_rows:
                clue = clues[x]

                if self.get(x, M-1, transpose) == 1:
                    for dy in range(1, clue[-1]):
                        self.set(x, M-1 - dy, 1, changed, transpose)

                    next = M-1 - clue[-1]
                    if next >= 0:
                        self.set(x, next, 0, changed, transpose)

                # TODO: handle left case





        print(changed)
        self.print()







    def solve(self):
        self.print_clues()
        self.print()

        changed = self.deduce_initial()

        print(changed)
        self.print()


        self.deduce(changed)


        pass










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

res = n.solve()

print("===================== RESULT")
print(res)


print("==> Duration:", time() - start)



