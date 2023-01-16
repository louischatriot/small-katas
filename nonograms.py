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
    def __init__(self, clues, clone=False):
        self.colclues = clues[0]
        self.rowclues = clues[1]
        self.N = len(self.rowclues)
        self.M = len(self.colclues)

        if not clone:
            self.grid = [['?' for _ in range(0, self.M)] for _ in range(0, self.N)]
            self.row_set = [0 for _ in range(0, self.N)]
            self.col_set = [0 for _ in range(0, self.M)]
            self.todo = self.M * self.N

            self.row_to_fill = [sum(clue) for clue in self.rowclues]
            self.col_to_fill = [sum(clue) for clue in self.colclues]
            self.row_to_empty = [self.M - sum(clue) for clue in self.rowclues]

            self.done_up_to = {
                False: { 'left': [0 for _ in range(0, self.M)], 'right': [self.M - 1 for _ in range(0, self.M)] },
                True: { 'left': [0 for _ in range(0, self.N)], 'right': [self.N - 1 for _ in range(0, self.N)] }
            }
            self.clue_done_up_to = {
                False: { 'left': [0 for _ in range(0, self.M)], 'right': [0 for _ in range(0, self.M)] },
                True: { 'left': [0 for _ in range(0, self.N)], 'right': [0 for _ in range(0, self.N)] }
            }


    def clone(self):
        n = Nonogram((self. colclues, self.rowclues), True)
        n.grid = [[c for c in line] for line in self.grid]
        n.row_set = [c for c in self.row_set]
        n.col_set = [c for c in self.col_set]
        n.todo = self.todo
        n.done_up_to = {
            False: { 'left': [i for i in self.done_up_to[False]['left']], 'right': [i for i in self.done_up_to[False]['right']] },
            True: { 'left': [i for i in self.done_up_to[True]['left']], 'right': [i for i in self.done_up_to[True]['right']] }
        }

        n.clue_done_up_to = {
            False: { 'left': [i for i in self.clue_done_up_to[False]['left']], 'right': [i for i in self.clue_done_up_to[False]['right']] },
            True: { 'left': [i for i in self.clue_done_up_to[True]['left']], 'right': [i for i in self.clue_done_up_to[True]['right']] }
        }

        n.row_to_fill = [i for i in self.row_to_fill]
        n.col_to_fill = [i for i in self.col_to_fill]
        n.row_to_empty = [i for i in self.row_to_empty]

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

            self.row_set[x] += 1
            if self.row_set[x] == self.M:
                self.check_correct(x, None)

            self.col_set[y] += 1
            if self.col_set[y] == self.N:
                self.check_correct(None, y)

            # TODO: check correctedness here
            # TODO: only add columns to changed and check full line here only to remove the above code
            if value == 1:
                self.row_to_fill[x] -= 1
                if self.row_to_fill[x] == 0:
                    for yy in range(0, self.M):
                        if self.grid[x][yy] == '?':
                            self.set(x, yy, 0, changed, False)

                self.col_to_fill[y] -= 1
                if self.col_to_fill[y] == 0:
                    for xx in range(0, self.N):
                        if self.grid[xx][y] == '?':
                            self.set(xx, y, 0, changed, False)

            # if value == 0:
                # self.row_to_empty[x] -= 1

                # if self.row_to_empty[x] == 0:
                    # for yy in range(0, self.M):
                        # if self.grid[x][yy] == '?':
                            # self.set(x, yy, 1, changed, False)

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
        # for clues, transpose, the_rows, M in [(self.rowclues, False, rows, self.M), (self.colclues, True, cols, self.N)]:
            # for x in the_rows:
                # clue = clues[x]

                # if sum([1 if self.get(x, y, transpose) == 1 else 0 for y in range(0, M)]) == sum(clue):
                    # for y in range(0, M):
                        # if self.get(x, y, transpose) == '?':
                            # self.set(x, y, 0, changed, transpose)

                # This one is actually useless ...
                # if sum([1 if self.get(x, y, transpose) == 0 else 0 for y in range(0, M)]) == M - sum(clue):
                    # for y in range(0, M):
                        # if self.get(x, y, transpose) == '?':
                            # self.set(x, y, 1, changed, transpose)


        # When one filled square is close to a border
        # Only case handled for now = glued to a border
        for clues, transpose, the_rows, M in [(self.rowclues, False, rows, self.M), (self.colclues, True, cols, self.N)]:
            for x in the_rows:
                clue = clues[x]

                # Left
                l = self.done_up_to[transpose]['left'][x]
                for cn, c in enumerate(clue):
                    if cn < self.clue_done_up_to[transpose]['left'][x]:
                        continue

                    for l in range(l, M):
                        if self.get(x, l, transpose) != 0:
                            break

                    # Could keep track of done clues to avoid re setting the same cell over and over again ...
                    if self.get(x, l, transpose) != 1:
                        break

                    for dy in range(1, c):
                        self.set(x, l + dy, 1, changed, transpose)

                    l += c

                    self.done_up_to[transpose]['left'][x] = l+1
                    self.clue_done_up_to[transpose]['left'][x] = cn+1

                    if l < M:
                        self.set(x, l, 0, changed, transpose)


                # Right
                r = self.done_up_to[transpose]['right'][x]
                for cn, c in enumerate(reversed(clue)):
                    if cn < self.clue_done_up_to[transpose]['right'][x]:
                        continue

                    for r in range(r, -1, -1):
                        if self.get(x, r, transpose) != 0:
                            break

                    if self.get(x, r, transpose) != 1:
                        break

                    for dy in range(1, c):
                        self.set(x, r - dy, 1, changed, transpose)

                    r -= c

                    self.done_up_to[transpose]['right'][x] = r-1
                    self.clue_done_up_to[transpose]['right'][x] = cn+1

                    if r >= 0:
                        self.set(x, r, 0, changed, transpose)


        # Check if first clue is constrained enough (by a wall or the grid)
        for clues, transpose, the_rows, M in [(self.rowclues, False, rows, self.M), (self.colclues, True, cols, self.N)]:
            for x in the_rows:
                clue = clues[x]

                # START FROM LEFT
                for pos_l in range(0, M):
                    if self.get(x, pos_l, transpose) != 0:
                        break

                # Last non wall space in contiguous box
                # Works as long as there is at least one clue / line is not full of x
                for pos_r in range(pos_l, M):
                    if self.get(x, pos_r, transpose) == 0:
                        break

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
                for pos_r in range(M-1, -1, -1):
                    if self.get(x, pos_r, transpose) != 0:
                        break

                for pos_l in range(pos_r, -1, -1):
                    if self.get(x, pos_l, transpose) == 0:
                        break

                if pos_l > 0:
                    pos_l += 1

                if any(self.get(x, y, transpose) == 1 for y in range(pos_l, pos_r+1)):
                    c = clue[-1]
                    movable = pos_r + 1 - pos_l - c

                    # Filling the middle
                    for y in range(pos_l + movable, pos_r - movable + 1):
                        self.set(x, y, 1, changed, transpose)

                    # From the right
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

        # self.set(14, 4, 1, changed, False)

        while len(changed) > 0 and self.todo > 0:
            changed = self.deduce(changed)

        print("========> AFTER DEDUCTIONS")
        self.print()


        print(self.done_up_to)
        print(self.clue_done_up_to)

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

                # if y % 2 == 0:
                    # y0 = y // 2
                # else:
                    # y0 = self.M - y // 2 - 1

                # if self.grid[x0][y0] == '?':
                    # return (x0, y0)




        else:
            for x in range(0, self.N):
                if self.grid[x][y0] == '?':
                    return (x, y0)

                # if x % 2 == 0:
                    # x0 = x // 2
                # else:
                    # x0 = self.N - x // 2 - 1

                # if self.grid[x0][y0] == '?':
                    # return (x0, y0)






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

        for g in [0, 1]:

            if sum([1 if i == 0 else 0 for i in self.grid[x]]) >= self.M - sum(self.rowclues[x]) and g == 0:
                continue

            if sum([1 if self.grid[xx][y] == 0 else 0 for xx in range(0, self.N)]) >= self.N - sum(self.colclues[y]) and g == 0:
                continue



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







