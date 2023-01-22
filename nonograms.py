from time import time



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


        self.changed = set()

        if not clone:
            self.grid = [[2 for _ in range(0, self.M)] for _ in range(0, self.N)]
            self.row_set = [0 for _ in range(0, self.N)]
            self.col_set = [0 for _ in range(0, self.M)]
            self.todo = self.M * self.N

            self.rowboundaries = [tuple((sum(clues[0:i]) + i, self.M - sum(clues[i:]) - (len(clues) - 1 - i)) for i in range(0, len(clues))) for clues in self.rowclues]
            self.colboundaries = [tuple((sum(clues[0:i]) + i, self.N - sum(clues[i:]) - (len(clues) - 1 - i)) for i in range(0, len(clues))) for clues in self.colclues]

            self.done_up_to = {
                False: { 'left': [0 for _ in range(0, self.M)], 'right': [self.M - 1 for _ in range(0, self.M)] },
                True: { 'left': [0 for _ in range(0, self.N)], 'right': [self.N - 1 for _ in range(0, self.N)] }
            }
            self.clue_done_up_to = {
                False: { 'left': [0 for _ in range(0, self.M)], 'right': [0 for _ in range(0, self.M)] },
                True: { 'left': [0 for _ in range(0, self.N)], 'right': [0 for _ in range(0, self.N)] }
            }

    def reset_changed(self):
        self.changed = set()

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

        n.rowboundaries = [i for i in self.rowboundaries]
        n.colboundaries = [i for i in self.colboundaries]

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


    def set(self, x, y, value, transpose = False):
        if transpose:
            x, y = y, x

        if value == self.grid[x][y]:
            return True

        if self.grid[x][y] == 2:
            self.grid[x][y] = value
            self.changed.add((x, y))

            self.todo -= 1

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
        # Cannot slide much
        for clues, transpose, M in [(self.rowclues, False, self.M), (self.colclues, True, self.N)]:
            for x, clue in enumerate(clues):
                movable = M - sum(clue) - (len(clue) - 1)

                if movable == 0:
                    y = 0
                    for _ in range(0, clue[0]):
                        self.set(x, y, 1, transpose)
                        y += 1

                    for c in clue[1:]:
                        self.set(x, y, 0, transpose)
                        y += 1

                        for _ in range(0, c):
                            self.set(x, y, 1, transpose)
                            y += 1

                else:
                    for i, c in enumerate(clue):
                        if c > movable:
                            before = sum(clue[0:i]) + len(clue[0:i])
                            for dy in range(0, c - movable):
                                self.set(x, before + movable + dy, 1, transpose)





    def left_most(self, x, M, clue, boundary, transpose, i_start, idx):
        c = clue[idx]
        bl, bh = boundary[idx]

        i0 = max(bl, i_start)
        while i0 <= bh:
            if all(self.get(x, i, transpose) in [1, 2] for i in range(i0, i0 + c)):
                if idx == len(clue) - 1:
                    if all(self.get(x, i, transpose) in [0, 2] for i in range(i0 + c, M)):
                        return [i0]

                else:
                    if self.get(x, i0 + c, transpose) in [0, 2]:
                        tail = self.left_most(x, M, clue, boundary, transpose, i0 + c + 1, idx + 1)
                        if tail:
                            return [i0] + tail

            if self.get(x, i0, transpose) == 1:
                break
            else:
                i0 += 1

        return None


    def right_most(self, x, M, clue, boundary, transpose, i_start, idx):
        c = clue[idx]
        bl, bh = boundary[idx]

        i0 = min(bh, i_start)
        while i0 >= bl:
            if all(self.get(x, i, transpose) in [1, 2] for i in range(i0, i0 + c)):
                if idx == 0:
                    if all(self.get(x, i, transpose) in [0, 2] for i in range(0, i0)):
                        return [i0]

                else:
                    if self.get(x, i0 - 1, transpose) in [0, 2]:
                        tail = self.right_most(x, M, clue, boundary, transpose, i0 - clue[idx-1] - 1, idx - 1)
                        if tail:
                            return tail + [i0]

            if self.get(x, i0 + c - 1, transpose) == 1:
                break
            else:
                i0 -= 1

        return None


    def deduce(self):
        rows, cols = get_rows_and_cols(self.changed)
        self.reset_changed()

        for clues, boundaries, transpose, the_rows, M in [(self.rowclues, self.rowboundaries, False, rows, self.M), (self.colclues, self.colboundaries, True, cols, self.N)]:
            for x in the_rows:
                clue = clues[x]
                boundary = boundaries[x]

                if len(clue) == 0:
                    continue   # Nothing to learn

                left = self.left_most(x, M, clue, boundary, transpose, 0, 0)

                if left is None:
                    raise ValueError("Wrong guess earlier")

                right = self.right_most(x, M, clue, boundary, transpose, M - 1, len(clue) - 1)

                for l, r, c in zip(left, right, clue):
                    for i in range(max(l, r), min(l, r) + c):
                        self.set(x, i, 1, transpose)

                for i in range(0, left[0]):
                    self.set(x, i, 0, transpose)

                for i in range(right[-1] + clue[-1], M):
                    self.set(x, i, 0, transpose)

                for idx in range(1, len(clue)):
                    for i in range(right[idx - 1] + clue[idx - 1], left[idx]):
                        self.set(x, i, 0, transpose)



    def solve(self):
        self.deduce_initial()

        while len(self.changed) > 0 and self.todo > 0:
            self.deduce()

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
                if self.grid[x0][y] == 2:
                    return (x0, y)

        else:
            for x in range(0, self.N):
                if self.grid[x][y0] == 2:
                    return (x, y0)


    def guess(self, t=0):
        done = False
        for x in range(0, self.N):
            for y in range(0, self.M):
                if self.grid[x][y] == 2:
                    done = True
                if done:
                    break
            if done:
                break

        # x, y = self.next_guess()

        for g in [0, 1]:
            n = self.clone()

            try:
                n.set(x, y, g, False)
                while len(n.changed) > 0:
                    n.deduce()
            except:
                continue   # Wrong guess

            if n.todo == 0:
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





clues = (((), (4, 1), (11,), (2, 4), (2, 5), (9,), (10,), (10,), (11,), (12,), (10,), (3, 3), (8,), (5,), (1,)), ((1,), (3,), (6,), (10,), (11,), (1, 8), (1, 7, 1), (9, 1), (13,), (13,), (13,), (2, 4, 2), (1, 2), (2,), ()))








start = time()

n = Nonogram(clues)

res = n.solve()

print(n.row_set)
print(n.col_set)

print("===================== RESULT")
print(res)
n.print()


if res == ans:
    print("FUCK YEAH")
else:
    print("OH NOES")


print("==> Duration:", time() - start)


1/0


# print(n.rowclues)
# print(n.colclues)
# n.print()
# print(n.row_set)
# print(n.col_set)



# print("==========================================")
# print("==========================================")








def left_most(line, clues, boundaries, i_start, idx):
    c = clues[idx]
    bl, bh = boundaries[idx]

    i0 = max(bl, i_start)
    while i0 <= bh:
        if all(line[i] in [1, 2] for i in range(i0, i0 + c)):
            if idx == len(clues) - 1:
                if all(line[i] in [0, 2] for i in range(i0 + c, len(line))):
                    return [i0]

            else:
                if line[i0 + c] in [0, 2]:
                    tail = left_most(line, clues, boundaries, i0 + c + 1, idx + 1)
                    if tail:
                        return [i0] + tail

        if line[i0] == 1:
            break
        else:
            i0 += 1

    return None


def right_most(line, clues, boundaries, i_start, idx):
    c = clues[idx]
    bl, bh = boundaries[idx]

    i0 = min(bh, i_start)
    while i0 >= bl:
        if all(line[i] in [1, 2] for i in range(i0, i0 + c)):
            if idx == 0:
                if all(line[i] in [0, 2] for i in range(0, i0)):
                    return [i0]

            else:
                if line[i0 - 1] in [0, 2]:
                    tail = right_most(line, clues, boundaries, i0 - clues[idx-1] - 1, idx - 1)
                    if tail:
                        return tail + [i0]

        if line[i0 + c - 1] == 1:
            break
        else:
            i0 -= 1

    return None







line = [2 for i in range(0, 15)]
clues = (4, 5, 2)

boundaries = tuple((sum(clues[0:i]) + i, len(line) - sum(clues[i:]) - (len(clues) - 1 - i)) for i in range(0, len(clues)))
print(boundaries)


line[14] = 1
line[11] = 1
# line[2] = 0
# line[3] = 1
# line[6] = 0
# line[7] = 1
# line[8] = 1
# line[10] = 1


print(line)
print(clues)


left = left_most(line, clues, boundaries, 0, 0)
right = right_most(line, clues, boundaries, len(line) - 1, len(clues) - 1)

print(left)
print(right)

for l, r, c in zip(left, right, clues):
    for i in range(max(l, r), min(l, r) + c):
        line[i] = 1

for i in range(0, left[0]):
    line[i] = 0

for i in range(right[-1] + clues[-1], len(line)):
    line[i] = 0

for idx in range(1, len(clues)):
    for i in range(right[idx - 1] + clues[idx - 1], left[idx]):
        line[i] = 0

print(line)









