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

        self.row_set = [0 for _ in range(0, self.N)]
        self.col_set = [0 for _ in range(0, self.M)]

        # TODO: check if next_in_line is enough
        self.todo = self.M * self.N
        self.next_in_line = 0


    def clone(self):
        n = Nonogram((self. colclues, self.rowclues))
        n.grid = [[c for c in line] for line in self.grid]
        n.row_set = [c for c in self.row_set]
        n.col_set = [c for c in self.col_set]
        n.todo = self.todo
        n.next_in_line = self.next_in_line
        return n


    def print(self):
        print('\n'.join([' '.join(['[]' if c == 1 else ('x ' if c == 0 else '. ') for c in l]) + '   ' + ','.join([str(c) for c in self.rowclues[x]]) for x, l in enumerate(self.grid)]))
        print('')
        for ci in range(0, max([len(c) for c in self.colclues])):
            l = ''
            for c in self.colclues:
                l += (str(c[ci]) if ci < len(c) else ' ') + '  '
            print(l)
        print("========================================================")


    def print_clues(self):
        print("ROW CLUES:", self.rowclues)
        print("COL CLUES:", self.colclues)
        print("========================================================")


    # Should only be called with complete lines
    def check_correct(self, row = None, col = None):
        clues = self.rowclues[row] if row is not None else self.colclues[col]
        line = [c for c in self.grid[row]] if row is not None else [self.grid[x][col] for x in range(0, self.N)]

        line.append(0)
        deduced_clues = []
        current = 0
        for c in line:
            if c == 1:
                current += 1
            else:
                if current != 0:
                    deduced_clues.append(current)
                    current = 0

        if tuple(deduced_clues) != clues:
            raise ValueError("Clue not matched")


    def set(self, x, y, value, changed, transpose = False):
        if transpose:
            x, y = y, x

        if value == self.grid[x][y]:
            return True

        if self.grid[x][y] == '?':
            self.grid[x][y] = value
            changed.add((x, y))

            self.todo -= 1
            self.next_in_line = max(self.next_in_line, x * self.M + y + 1)

            self.row_set[x] += 1
            if self.row_set[x] == self.M:
                self.check_correct(x, None)

            self.col_set[y] += 1
            if self.col_set[y] == self.N:
                self.check_correct(None, y)

            return True

        raise ValueError("Incompatibility")


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
        changed = set()

        # Check if row is already done
        for clues, transpose, the_rows, M in [(self.rowclues, False, rows, self.M), (self.colclues, True, cols, self.N)]:
            for x in the_rows:
                clue = clues[x]

                if sum([1 if self.get(x, y, transpose) == 1 else 0 for y in range(0, M)]) == sum(clue):
                    for y in range(0, M):
                        if self.get(x, y, transpose) == '?':
                            self.set(x, y, 0, changed, transpose)


        # When one filled square is close to a border
        # Only case handled for now = glued to a border
        for clues, transpose, the_rows, M in [(self.rowclues, False, rows, self.M), (self.colclues, True, cols, self.N)]:
            for x in the_rows:
                clue = clues[x]

                # Left
                l = 0
                for c in clue:
                    for l in range(l, M):
                        if self.get(x, l, transpose) != 0:
                            break

                    # Could keep track of done clues to avoid re setting the same cell over and over again ...
                    if self.get(x, l, transpose) != 1:
                        break

                    for dy in range(1, c):
                        self.set(x, l + dy, 1, changed, transpose)

                    l += c
                    if l < M:
                        self.set(x, l, 0, changed, transpose)


                # Right
                r = M - 1
                for c in reversed(clue):
                    for r in range(r, -1, -1):
                        if self.get(x, r, transpose) != 0:
                            break

                    if self.get(x, r, transpose) != 1:
                        break

                    for dy in range(1, c):
                        self.set(x, r - dy, 1, changed, transpose)

                    r -= c
                    if r >= 0:
                        self.set(x, r, 0, changed, transpose)


        # Check if first clue is constrained enough (by a wall or the grid)
        for clues, transpose, the_rows, M in [(self.rowclues, False, rows, self.M), (self.colclues, True, cols, self.N)]:
            for x in the_rows:
                clue = clues[x]

                # First non wall space
                for pos_l in range(0, M):
                    if self.get(x, pos_l, transpose) != 0:
                        break

                # Last non wall space in contiguous box
                # Works as long as there is at least one clue / line is not full of x
                for pos_r in range(pos_l, M):
                    if self.get(x, pos_r, transpose) == 0:
                        break

                # TODO: WTF
                if pos_r < M-1:
                    pos_r -= 1

                # TODO: check if mistake here, and should only use if the filled square is central enough
                if any(self.get(x, y, transpose) == 1 for y in range(pos_l, pos_r+1)):
                    c = clue[0]
                    movable = pos_r + 1 - pos_l - c

                    # Filling the middle
                    for y in range(pos_l + movable, pos_r - movable + 1):
                        self.set(x, y, 1, changed, transpose)

                    # Clue close to the left
                    for y0 in range(0, c-1):
                        if self.get(x, y0, transpose) == 1:
                            for y in range(y0, c):
                                self.set(x, y, 1, changed, transpose)


                # START FROM RIGHT
                # TODO: case where we start from the right
                for pos_r in range(M-1, -1, -1):
                    if self.get(x, pos_r, transpose) != 0:
                        break

                for pos_l in range(pos_r, -1, -1):
                    if self.get(x, pos_l, transpose) == 0:
                        break

                # TODO: WTF
                if pos_l > 0:
                    pos_l += 1

                if any(self.get(x, y, transpose) == 1 for y in range(pos_l, pos_r+1)):
                    c = clue[-1]
                    movable = pos_r + 1 - pos_l - c

                    # Filling the middle
                    for y in range(pos_l + movable, pos_r - movable + 1):
                        self.set(x, y, 1, changed, transpose)

                    # From the right, TODO FIX
                    for y0 in range(M-1, M-1 - (c-1), -1):
                        if self.get(x, y0, transpose) == 1:
                            for y in range(y0, M-1 - c, -1):
                                self.set(x, y, 1, changed, transpose)



        # TODO: Check if spacing gives us enough information to put some x


        return changed


    def solve(self):
        self.print_clues()
        self.print()

        changed = self.deduce_initial()

        self.print()

        while len(changed) > 0 and self.todo > 0:
            changed = self.deduce(changed)

        print("========> AFTER DEDUCTIONS")
        self.print()

        if self.todo == 0:
            res = self.grid
        else:
            res = self.guess()

        res = tuple([tuple(l) for l in res])
        return res


    # Actually worse than before, let's check if it's because it's buggy or a bad idea
    def next_guess(self):
        for xu in range(0, self.N):
            if self.row_set[xu] < self.M:
                break

        for xb in range(self.N - 1, -1, -1):
            if self.row_set[xb] < self.M:
                break

        x0 = xu if self.row_set[xu] > self.row_set[xb] else xb

        for yu in range(0, self.M):
            if self.col_set[yu] < self.N:
                break

        for yb in range(self.M - 1, -1, -1):
            if self.col_set[yb] < self.N:
                break

        y0 = yu if self.col_set[yu] > self.col_set[yb] else yb

        if self.row_set[x0] > self.col_set[y0]:
            for y in range(0, self.M):
                if self.grid[x0][y] == '?':
                    return (x0, y)
        else:
            for x in range(0, self.N):
                if self.grid[x][y0] == '?':
                    return (x, y0)


        raise ValueError("WAAAAAAT")


        # TODO: keep track of the next instead of looping on the entire grid like an idiot
        # Also, assuming a square shape for now
        for round in range(0, self.N // 2):
            for y in range(round, self.N - round):
                if self.grid[round][y] == '?':
                    return (round, y)

            for x in range(round + 1, self.N - round):
                if self.grid[x][round] == '?':
                    return (x, round)

            for y in range(self.N - 1 - round, round - 1, -1):
                if self.grid[round][y] == '?':
                    return (round, y)

            for x in range(self.N - 2 - round, round, -1):
                if self.grid[x][round] == '?':
                    return (x, round)

        # Base case
        for x in range(0, self.N):
            for y in range(0, self.M):
                if self.grid[x][y] == '?':
                    return (x, y)



    def guess(self, t=0):
        x, y = self.next_guess()


        # done = False
        # # for x in range(0, self.N):
        # for x in range(self.N - 1, -1, -1):
            # for y in range(0, self.M):
                # if self.grid[x][y] == '?':
                    # done = True
                # if done:
                    # break
            # if done:
                # break

        for g in [1, 0]:
            n = self.clone()
            changed = set()

            try:
                n.set(x, y, g, changed, False)
                while len(changed) > 0:
                    changed = n.deduce(changed)
            except:
                continue   # Wrong guess

            if n.todo == 0:
                n.print()
                return n.grid

            res = n.guess(t+1)
            if res is not None:
                return res


        return None


def solve(clues):
    n = Nonogram(clues)
    return n.solve()








clues = (
    ((1, 1), (4,), (1, 1, 1), (3,), (1,)),
    ((1,), (2,), (3,), (2, 1), (4,))
)

ans = ((0, 0, 1, 0, 0),
       (1, 1, 0, 0, 0),
       (0, 1, 1, 1, 0),
       (1, 1, 0, 1, 0),
       (0, 1, 1, 1, 1))


# Puppy
clues = (
    (
        (4, 3), (1, 6, 2), (1, 2, 2, 1, 1), (1, 2, 2, 1, 2), (3, 2, 3),
        (2, 1, 3), (1, 1, 1), (2, 1, 4, 1), (1, 1, 1, 1, 2), (1, 4, 2),
        (1, 1, 2, 1), (2, 7, 1), (2, 1, 1, 2), (1, 2, 1), (3, 3)
    ), (
        (3, 2), (1, 1, 1, 1), (1, 2, 1, 2), (1, 2, 1, 1, 3), (1, 1, 2, 1),
        (2, 3, 1, 2), (9, 3), (2, 3), (1, 2), (1, 1, 1, 1),
        (1, 4, 1), (1, 2, 2, 2), (1, 1, 1, 1, 1, 1, 2), (2, 1, 1, 2, 1, 1), (3, 4, 3, 1)
    )
)

ans = (
    (0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0),
    (0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0),
    (1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0),
    (1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1),
    (1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1),
    (1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1),
    (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0),
    (0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0),
    (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0),
    (0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0),
    (0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0),
    (1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0),
    (1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1),
    (1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1),
    (0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1)
)


# Car
clues = (((2,), (8,), (3, 2), (6, 2, 2), (1, 1, 1, 1), (1, 2, 1, 1, 1, 1), (1, 1, 2, 1, 1, 1), (1, 1, 1, 1), (1, 1, 1, 1, 1), (1, 4, 1, 1, 1), (1, 1, 1, 1), (6, 2, 2), (3, 2), (8,), (2,)), ((7,), (1, 1), (1, 2, 2, 1), (1, 1, 1, 1), (1, 1, 1, 1), (1, 2, 1, 1), (4, 4), (3, 7, 3), (3, 3), (1, 9, 1), (1, 1), (1, 1), (1, 9, 1), (3, 3), (1, 1)))


# Stroller
clues = (((2, 3, 3), (5, 6, 1), (1, 4, 4), (1, 2, 2, 3), (1, 1, 3), (1, 4), (2, 1), (2,), (3, 1), (3, 1, 3), (1, 1, 1, 2, 2), (1, 1, 1, 1, 1, 1), (2, 1, 1, 2, 2), (3, 1, 3), (3, 1)), ((3,), (2, 1), (4, 3), (3, 1, 2), (2, 1, 1), (1, 2, 2, 1), (1, 1, 1, 2, 1), (2, 3, 1, 1), (3, 9), (3, 1), (4, 1, 3, 1), (2, 2, 2, 2), (2, 2, 1, 1, 1), (1, 1, 2, 2), (2, 2, 3)))



# 38 ms
clues = (((2, 3, 2, 1), (1, 1, 1, 2, 1, 2), (1, 1, 1, 2, 1), (1, 3, 3), (1, 1, 1, 3, 1, 2), (1, 1, 1, 1, 1, 1), (2, 3, 4, 1), (1, 1, 3, 1), (6, 1, 1, 1), (2, 2, 2), (1, 2, 4, 2), (1, 1, 1, 1, 2), (2, 3, 2), (2, 2, 3, 1), (3, 4)), ((2, 2, 4), (1, 3, 1, 2, 2), (1, 1, 1, 2), (1, 1, 1, 1, 1, 2, 1), (1, 1, 1, 1, 2), (1, 3, 1, 1, 3), (1, 1, 1, 3, 1), (3, 2, 2), (2, 1, 1, 1, 1), (1, 2, 1, 1, 4), (2, 3, 1, 1), (2, 2, 2, 1, 2), (1, 4, 2, 1), (1, 1, 2, 1), (2, 6, 1)))


# 2s
clues = (((1, 1, 1), (1, 1, 1, 1), (1, 2, 1, 1), (2, 3, 2, 1), (1, 4, 1, 3), (1, 3, 2, 2), (1, 7, 2, 1), (1, 3, 1, 3), (1, 1, 3, 1, 2), (2, 2, 2), (2, 1, 3), (1, 2, 2), (1, 2, 2), (3, 7), (2,)), ((3,), (1, 1), (1, 1), (1, 4, 4), (4, 2, 1), (2, 3, 2, 2), (1, 2, 1, 1, 2, 1), (3, 1, 4, 2), (4, 1, 1, 2), (1, 1, 3), (2, 1, 2, 1), (2, 2, 1, 1), (1, 2, 2, 2, 1), (1, 2, 3, 1), (8,)))





start = time()

n = Nonogram(clues)

res = n.solve()

print(n.row_set)
print(n.col_set)

print("===================== RESULT")
print(res)


if res == ans:
    print("FUCK YEAH")
else:
    print("OH NOES")


print("==> Duration:", time() - start)


# print(n.rowclues)
# print(n.colclues)
# n.print()
# print(n.row_set)
# print(n.col_set)


# GGG = n.clone()

# print("==========================================")
# print("==========================================")


# print(GGG.rowclues)
# print(GGG.colclues)
# GGG.print()
# print(GGG.row_set)
# print(GGG.col_set)







