from time import time

cache = dict()
other_cache = dict()

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

        self.reset_changed()

        if not clone:
            self.grid = [[2 for _ in range(0, self.M)] for _ in range(0, self.N)]
            self.row_set = [0 for _ in range(0, self.N)]
            self.col_set = [0 for _ in range(0, self.M)]
            self.todo = self.M * self.N
            self.rowboundaries = [list((sum(clues[0:i]) + i, self.M - sum(clues[i:]) - (len(clues) - 1 - i)) for i in range(0, len(clues))) for clues in self.rowclues]
            self.colboundaries = [list((sum(clues[0:i]) + i, self.N - sum(clues[i:]) - (len(clues) - 1 - i)) for i in range(0, len(clues))) for clues in self.colclues]

    def pre_reset(self):
        return (self.changed_rows, self.changed_cols)


    def reset_changed(self):
        self.changed = set()
        self.changed_rows = set()
        self.changed_cols = set()


    def to_check(self):
        return len(self.changed_rows) > 0 or len(self.changed_cols) > 0

    def clone(self):
        n = Nonogram((self. colclues, self.rowclues), True)
        n.grid = [[c for c in line] for line in self.grid]
        n.row_set = [c for c in self.row_set]
        n.col_set = [c for c in self.col_set]
        n.todo = self.todo
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

            self.changed_cols.add(y)
            self.changed_rows.add(x)

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


    # Code here is much harder to follow than for right_most but about 50% more efficient
    # Tests pass without having to rewrite right_most which would be a pain :)
    def left_most(self, x, M, clue, boundary, transpose, i_start, idx):
        line = ''.join([str(self.get(x, i, transpose)) for i in range(i_start, M)])
        zc = '-'.join([str(c) for c in clue[idx:]])
        key = line + '-' + zc

        if key in other_cache:
            res, start = other_cache[key]
            if res is None:
                return None
            res = [i + i_start - start for i in res]
            return res


        c = clue[idx]
        bl, bh = boundary[idx]
        res = None


        if idx == len(clue) - 1:
            gaps = []
            il = None
            ih = None
            s = max(bl, i_start)
            laste = s - 1

            for i in range(s, bh + 1):
                v = self.get(x, i, transpose)

                if v == 1:
                    if il is None:
                        il = i
                    ih = i

                if v == 0:
                    if i - 1 - laste >= c:
                        gaps.append((laste + 1, i - 1))
                        laste = i

            if M - laste >= c:
                gaps.append((laste + 1, M - 1))

            if il is None:
                il = s
                ih = s

            if ih - il + 1 <= c:
                for gl, gh in gaps:
                    if gl <= il <= ih <= gh:
                        res = [max(gl, ih - c + 1)]
                        other_cache[key] = (res, i_start)
                        return res

            other_cache[key] = (None, i_start)
            return None

        else:
            s = max(bl, i_start)
            lastz = s - 1
            i = s

            # The zeroes
            while i < bh + c:
                v = self.get(x, i, transpose)

                if v == 1:
                    break
                elif v == 0:
                    lastz = i
                else:
                    if i - lastz >= c:
                        if self.get(x, i + 1, transpose) in [0, 2]:
                            tail = self.left_most(x, M, clue, boundary, transpose, i + 2, idx + 1)
                            if tail:
                                res = [i - c + 1] + tail
                                other_cache[key] = (res, i_start)
                                return res

                        else:
                            i += 1
                            break

                i += 1

            if lastz >= bh or i == bh + c:
                other_cache[key] = (None, i_start)
                return None

            # The ones
            first_one = i
            max_i = min(bh, first_one) + c - 1

            while i <= max_i:
                while self.get(x, i, transpose) == 1:
                    i += 1
                    if i == max_i + 1:
                        if self.get(x, i, transpose) == 1:
                            other_cache[key] = (None, i_start)
                            return None
                        else:
                            tail = self.left_most(x, M, clue, boundary, transpose, i + 1, idx + 1)
                            if tail:
                                res = [i - c] + tail
                                other_cache[key] = (res, i_start)
                                return res
                            else:
                                other_cache[key] = (None, i_start)
                                return None

                v = self.get(x, i, transpose)
                if v in [0, 2]:
                    if i - 1 - lastz >= c:

                        tail = self.left_most(x, M, clue, boundary, transpose, i + 1, idx + 1)

                        if tail:
                            res = [i - c] + tail
                            other_cache[key] = (res, i_start)
                            return res

                    if v == 0:
                        other_cache[key] = (None, i_start)
                        return None

                while i <= lastz + c:
                    if self.get(x, i, transpose) == 0 or i == max_i + 1:
                        other_cache[key] = (None, i_start)
                        return None

                    i += 1

                v = self.get(x, i, transpose)

                if v in [0, 2]:
                    tail = self.left_most(x, M, clue, boundary, transpose, i + 1, idx + 1)

                    if tail:
                        res = [i - c] + tail
                        other_cache[key] = (res, i_start)
                        return res
                    elif v == 0:
                        other_cache[key] = (None, i_start)
                        return None
                    else:
                        i += 1

                else:
                    continue



            other_cache[key] = (None, i_start)
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
        global cache

        rows, cols = self.changed_rows, self.changed_cols
        self.reset_changed()

        for clues, boundaries, transpose, the_rows, M, rs in [(self.rowclues, self.rowboundaries, False, rows, self.M, self.row_set), (self.colclues, self.colboundaries, True, cols, self.N, self.col_set)]:
            for x in the_rows:
                clue = clues[x]
                boundary = boundaries[x]

                if len(clue) == 0:
                    for i in range(0, M):
                        self.set(x, i, 0, transpose)

                    continue

                line = ''.join(str(self.get(x, i, transpose)) for i in range(0, M))
                line += '  -  ' + '.'.join(str(c) for c in clue)

                cached = False
                if line in cache:
                    cached = True
                    left, right = cache[line]
                else:
                    left = self.left_most(x, M, clue, boundary, transpose, 0, 0)

                    if left is None:
                        raise ValueError("Wrong guess earlier")

                    right = self.right_most(x, M, clue, boundary, transpose, M - 1, len(clue) - 1)
                    cache[line] = (left, right)


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
        for i in range(0, max(self.N, self.M)):
            self.changed_rows.add(min(i, self.N - 1))
            self.changed_cols.add(min(i, self.M - 1))

        while self.to_check() and self.todo > 0:
            self.deduce()

        if self.todo == 0:
            res = self.grid
        else:
            res = self.guess()

        res = tuple([tuple(l) for l in res])
        return res


    def guess(self):
        done = False

        for x in range(0, self.N):
            for y in range(0, self.M):
                if self.grid[x][y] == 2 and len(self.rowclues[x]) > 0 and len(self.colclues[y]) > 0:
                    done = True
                if done:
                    break
            if done:
                break

        for g in [0, 1]:
            n = self.clone()

            try:
                n.set(x, y, g, False)
                while n.to_check() > 0:
                    n.deduce()
            except:
                continue   # Wrong guess


            if n.todo == 0:
                return n.grid

            res = n.guess()
            if res is not None:
                return res

        return None


def solve(clues, w, h):
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



clues = (((25,), (1, 1), (1, 2, 1), (1, 3, 1), (1, 5, 1), (1, 5, 1), (1, 7, 1), (1, 7, 1), (1, 7, 1), (1, 7, 1), (1, 7, 1), (1, 6, 1), (1, 5, 1), (1, 4, 1), (1, 5, 1), (1, 7, 1), (1, 7, 1), (1, 9, 1), (1, 6, 3, 1), (1, 8, 2, 2, 1), (1, 2, 1, 2, 3, 1, 1), (1, 2, 2, 4, 1, 2), (1, 3, 4, 1, 1, 4), (2, 1, 1, 1, 1, 1, 1), (2, 2, 1, 1, 2, 1), (1, 2, 2, 2, 2, 1), (1, 1, 4, 2, 1), (1, 3, 4, 1), (1, 3, 6, 1), (1, 9, 1), (1, 8, 1), (1, 6, 1), (1, 3, 1), (1, 1), (25,)), ((35,), (1, 2, 1), (1, 1, 1, 1), (1, 1, 2, 1), (1, 4, 1), (1, 2, 1), (1, 5, 2, 1), (1, 9, 5, 1, 1), (1, 18, 2, 1, 1, 1), (1, 24, 2, 1), (1, 17, 1, 4, 1), (1, 16, 4, 1, 3, 1), (1, 6, 6, 1, 1, 2, 1), (1, 3, 5, 2, 4, 1), (1, 1, 2, 1, 4, 1), (1, 2, 3, 6, 1), (1, 1, 9, 1), (1, 2, 8, 1), (1, 2, 5, 1), (1, 1, 1), (1, 2, 1), (1, 1, 1, 1), (1, 2, 1, 1), (1, 2, 1), (35,)))



# clues = (((1, 1), (4,), (1, 1, 1), (3,), (1,)), ((1,), (2,), (3,), (2, 1), (4,)))



# clues = (((2, 11), (3, 10), (6, 11), (3, 2, 10), (4, 1, 1, 5, 1), (5, 2, 2, 2, 2), (3, 1, 4, 3, 1), (1, 1, 2, 7), (4, 2, 6), (1, 2, 1, 5), (2, 1, 1, 2, 2), (1, 1, 5, 4, 4), (1, 4, 1, 4, 4), (1, 1, 4, 2, 11), (1, 11, 3), (2, 1, 9), (1, 1, 8, 4), (2, 5, 2, 5, 1), (6, 1, 2, 1), (7, 1, 1, 1, 1), (3, 3, 1, 1, 3), (1, 3, 4, 4, 2, 2), (4, 7, 1, 1), (5, 3, 3, 1, 1), (5, 1, 2, 1, 2)), ((3, 3, 1, 3), (3, 3, 1, 1, 4), (6, 1, 1, 2, 3), (4, 1, 1, 8), (4, 2, 7, 2), (1, 2, 3, 1), (4, 5), (3, 3, 4, 1, 1), (1, 1, 1, 1, 7), (4, 2, 1, 4), (1, 4, 3, 4), (1, 1, 1, 1, 5, 1), (6, 2, 6, 4), (5, 1, 3, 1, 4), (1, 1, 1, 5, 1, 5), (4, 8, 1, 1), (6, 9), (4, 1, 1, 6), (5, 2, 5), (9, 2, 1), (10, 2, 4, 1), (5, 3, 3, 3, 1), (5, 4, 4, 1), (4, 8, 2, 1), (5, 8, 1, 1, 1)))



clues = (((10,), (10,), (10,), (10,), (3, 4, 26), (3, 4, 26), (3, 31), (18, 2, 3), (19, 2, 3), (5, 6, 2, 3), (5, 6, 2, 3), (3, 6, 6, 2, 3), (3, 6, 6, 2, 3), (3, 4, 11, 3), (3, 4, 11, 3), (8, 10, 7, 3), (8, 10, 8, 3), (8, 10, 10), (8, 10, 10), (8, 10, 10), (8, 5, 10), (12, 10), (12, 17), (7, 3, 17), (7, 3, 12), (14, 3, 12), (14, 3, 3, 6), (14, 3, 3, 6, 1), (14, 3, 3, 6), (19, 1, 3, 6), (19, 3, 6), (4, 10, 12), (4, 10, 12), (4, 10, 12), (4, 29), (12, 14), (12, 1, 6, 4, 2), (12, 6, 4, 4), (12, 2, 6, 4, 4, 1), (12, 3, 6, 4, 3, 1), (12, 3, 6, 4, 2, 1), (12, 3, 14, 2, 1), (12, 1, 14, 1, 1), (12, 1, 1, 14, 4), (12, 1, 14, 4), (1, 1), (5,), (5,)), ((10,), (10,), (7, 10, 20), (7, 10, 20), (7, 10, 20), (4, 6, 20), (4, 6, 6, 10), (4, 6, 6, 10), (7, 10, 6, 10), (7, 23, 10), (15, 10, 10), (20, 24), (7, 5, 14), (9, 5, 14), (5, 20, 4, 1), (5, 20, 1, 4), (5, 8, 6, 9), (5, 8, 6, 2), (5, 20, 2), (5, 5, 22, 3), (5, 5, 22, 2), (5, 11), (11, 1, 11), (11, 7, 11), (11, 7, 11), (11, 8, 2, 4), (20, 2, 4), (20, 2, 4), (3, 23, 4), (3, 32), (3, 32), (22, 14), (22, 14), (3, 4, 4, 2), (3, 13, 2), (13, 13, 1, 3), (13, 13, 6), (13, 13, 4, 2), (3, 13, 3, 2), (13, 1, 2), (7,), (1,)))


clues = (((3,), (4, 3), (32,), (32,), (32,), (5, 19), (5, 4, 5, 8), (5, 1, 3, 8), (5, 1, 9), (2, 1, 9), (2, 1, 12), (2, 8, 6), (5, 8, 6), (21, 7), (21, 7), (21, 7), (33,), (6, 1, 3), (7, 21), (7, 21), (3, 1, 12, 4), (3, 9, 1, 4, 4), (2, 3, 19), (22, 10), (13, 3, 10), (2, 4, 3, 10), (2, 4, 7, 3), (2, 2, 1, 7, 3), (2, 4, 7, 3), (2, 9, 4, 3), (3, 1, 4, 3), (10, 1, 4, 3), (3, 3, 11), (2, 3, 3, 11), (2, 1, 3, 12)), ((4, 7), (4, 7), (7, 5, 4, 2, 1), (7, 5, 2, 2, 1), (7, 5, 2, 2, 1), (15, 2, 2, 1), (21, 2, 1), (4, 5, 1, 2, 1), (4, 5, 4, 1, 2), (4, 5, 11, 2), (3, 5, 1, 9), (3, 9, 4, 6), (3, 4, 12, 2), (3, 4, 6, 6), (3, 11, 1), (15, 3, 1, 1), (5, 13, 1), (5, 10, 2, 1), (5, 13), (4, 6, 11, 3), (5, 6, 11, 3), (5, 6, 11, 3), (15, 3, 1, 6), (9, 1, 2, 1, 6, 1), (9, 1, 2, 1, 9), (4, 3, 1, 2, 13), (9, 1, 2, 4, 3), (9, 1, 2, 4, 3), (15, 8, 3), (15, 8, 3), (15, 8, 3), (8, 7, 8, 3), (8, 7, 13), (8, 7, 13), (4, 13)))



clues = (((2, 2), (2, 5, 3), (5, 7, 3), (2, 7), (2, 2, 2, 2, 1), (2, 7, 2, 4, 2), (2, 4, 2, 2, 4, 2), (4, 2, 2, 7, 2), (2, 4, 2, 2, 7, 2), (2, 2, 2, 2, 1, 4, 1), (2, 2, 2, 2, 2, 1, 1, 1), (2, 3, 2, 1, 1), (2, 3, 2, 1, 1), (15, 4, 1), (7, 8, 4, 1), (7, 8, 4), (7, 8, 4), (6, 2, 3), (6, 2, 3, 8, 4), (6, 6, 8, 4), (1, 4, 6, 15), (1, 4, 3, 15), (1, 4, 3, 14), (13, 3, 14), (16, 4, 8), (22, 2), (4, 2, 3, 11), (4, 7, 11, 3), (4, 7, 6, 3, 3), (4, 7, 6, 3, 3), (2, 12, 3), (1, 12, 3), (1, 3), (4, 3), (3,)), ((4,), (4,), (4, 7), (3, 4, 7), (3, 4, 10), (2, 4, 8), (2, 13, 1), (1, 3, 3, 1), (2, 9, 13, 1), (2, 9, 13, 1), (4, 1, 9, 3), (2, 4, 13, 3), (2, 1, 6, 7), (2, 16, 7), (2, 16, 7), (2, 3, 2, 2), (12, 2), (1, 8, 18), (1, 8, 10, 7), (7,), (14,), (3, 14), (15, 14), (7, 4, 10, 2), (2, 4, 4, 6, 2, 2), (7, 4, 6, 6), (3, 2, 14), (2, 7, 14), (3, 3, 1, 5), (1, 1, 5), (2, 8, 5), (2, 4, 7, 8), (2, 2, 7, 8), (7, 8), (1, 4)))

clues = (((7,), (5,), (3,), (3,), (1,), (1,), (), (2, 1, 2, 2, 7), (3, 1, 3, 3, 7), (5, 1, 8, 7), (5, 8, 1, 4), (4, 6, 3), (2, 2, 1), (), (), (1, 2, 1), (2, 3), (1, 3), (2, 1), (1, 2), (1, 2, 1), (2, 3, 1), (2, 1, 1), (), (2, 2, 2, 2, 2, 2), (2, 2, 2, 2, 2, 2), (5, 5, 5), (3, 3, 3), (5, 5, 5), (3, 3, 2, 1, 2, 3, 3), (5, 5, 5), (), (9,), (2, 1, 1, 1, 2), (9,)), ((6, 1), (6, 2, 1, 1, 1), (4, 1, 2, 3, 3), (3, 5, 1, 5), (2, 1, 3, 1), (1, 1, 1, 2, 1, 5), (2, 6, 3, 3), (4, 3, 2, 1, 1), (6, 3, 1, 1), (4,), (2, 4), (1, 5, 1), (4, 2, 1), (4, 2, 3), (4, 3, 1), (4, 3, 5), (5, 3, 1), (4, 2, 3, 1), (2, 1, 3), (1, 1, 1), (3,), (1, 1), (3,), (4, 1, 1, 1, 1), (3, 3, 3, 3), (3, 1, 5, 1, 1), (4, 3, 1, 3), (6, 1, 5, 1), (5, 3, 3), (5, 1, 1)))



def launch():
    start = time()

    n = Nonogram(clues)

    res = n.solve()

    print(n.row_set)
    print(n.col_set)

    print("===================== RESULT")


    print(res)


    print("=============================================")
    print("=============================================")

    print('\n'.join([' '.join(['[]' if c == 1 else ('x ' if c == 0 else '. ') for c in l]) for x, l in enumerate(res)]))





    print("==> Duration:", time() - start)



launch()


# import cProfile
# cProfile.run('launch()')


