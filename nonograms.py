from time import time
import heapq

class Timer():
    def __init__(self):
        self.reset()

    def reset(self):
        self.start = time()
        self.events = {}
        self.current_events = {}

    def time(self, message = ''):
        duration = time() - self.start
        print(f"{message} ===> Duration: {duration}")
        self.reset()

    def start_event(self, evt):
        self.current_events[evt] = time()

    def stop_event(self, evt):
        if evt not in self.events:
            self.events[evt] = (0, 0)

        self.events[evt] = (self.events[evt][0] + time() - self.current_events[evt], self.events[evt][1] + 1)

    def print_events(self):
        for evt, v in self.events.items():
            print(f"{evt} - avg {v[0] / v[1]} - total {v[0]} - number {v[1]}")


t = Timer()


cache = dict()

threes = [3**i for i in range(0, 60)]



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
        # return len(self.changed) > 0

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


            # self.changed.add((x, y))


            if not transpose:
                self.changed_cols.add(y)
            else:
                # if self.row_set[x] < self.M:
                self.changed_rows.add(x)


            self.todo -= 1

            self.row_set[x] += 1
            if self.row_set[x] == self.M:
                self.check_correct(x, None)

            self.col_set[y] += 1
            if self.col_set[y] == self.N:
                self.check_correct(None, y)

            # t.stop_event('SET')
            return True


        raise ValueError("Incompatibility")


    def get(self, x, y, transpose = False):
        if transpose:
            x, y = y, x

        return self.grid[x][y]


    def left_most(self, x, M, clue, boundary, transpose, i_start, idx):
        c = clue[idx]
        bl, bh = boundary[idx]
        res = None



        if idx == len(clue) - 1:
            # t.start_event("LAST IDX")

            gaps = []
            il = None
            ih = None
            s = max(bl, i_start)
            laste = s - 1

            # TODO: CHECK IF ONLY WORKS BECAUSE BH IS M-1
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

            # print(il, ih, s, c)
            # print(gaps)

            if ih - il + 1 <= c:
                for gl, gh in gaps:
                    if gl <= il <= ih <= gh:
                        return [max(gl, ih - c + 1)]

            # TODO: stop the above loop once we look at gaps too far in the future? Or use a different data structure?


            return None


            for i in range(bestl, bh + 1):

                if v == 0 and il is None:
                    if i >= bestl + c - 1:
                        return [i]
                    else:
                        bestl = i


                if self.get(x, i, transpose) == 1:
                    if il is None:
                        il = i
                    ih = i

            if il is None and ih is None:
                return [bl]

            # TODO: FIX FIX
            if ih is None:
                return [max(bh, il - c + 1)]

            # TODO: FIX FIX
            if ih - il + 1 <= c:
                print(il, ih, c)
                return [max(bh, ih - c + 1)]
            else:
                return None




            i0 = max(bl, i_start)
            while i0 <= bh and res is None:
                if all(self.get(x, i, transpose) in [1, 2] for i in range(i0, i0 + c)):
                    if all(self.get(x, i, transpose) in [0, 2] for i in range(i0 + c, M)):
                        res = [i0]

                if self.get(x, i0, transpose) == 1:
                    break
                else:
                    i0 += 1

            # t.stop_event("LAST IDX")

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
                                return [i - c + 1] + tail

                        else:
                            i += 1
                            break

                i += 1

            if lastz >= bh or i == bh + c:
                return None

            # The ones
            first_one = i
            max_i = min(bh, first_one) + c - 1

            while i <= max_i:
                while self.get(x, i, transpose) == 1:
                    i += 1
                    if i == max_i + 1:
                        if self.get(x, i, transpose) == 1:
                            return None
                        else:
                            tail = self.left_most(x, M, clue, boundary, transpose, i + 1, idx + 1)
                            if tail:
                                return [i - c] + tail
                            else:
                                return None

                if self.get(x, i, transpose) == 0:
                    if i - 1 - lastz >= c:
                        tail = self.left_most(x, M, clue, boundary, transpose, i + 1, idx + 1)
                        if tail:
                            return [i - c] + tail

                    return None

                while i < lastz + c:
                    i += 1
                    if self.get(x, i, transpose) == 0 or i == max_i + 1:
                        return None

                i += 1
                v = self.get(x, i, transpose)

                if v in [0, 2]:
                    tail = self.left_most(x, M, clue, boundary, transpose, i + 1, idx + 1)
                    if tail:
                        return [i - c] + tail
                    elif v == 0:
                        return

                else:
                    continue



            return None

























            # i0 = max(bl, i_start)
            # while i0 <= bh and res is None:
                # if all(self.get(x, i, transpose) >= 1 for i in range(i0, i0 + c)):
                    # if self.get(x, i0 + c, transpose) in [0, 2]:
                        # tail = self.left_most(x, M, clue, boundary, transpose, i0 + c + 1, idx + 1)
                        # if tail:
                            # res = [i0] + tail

                # if self.get(x, i0, transpose) == 1:
                    # break
                # else:
                    # i0 += 1


        return res


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

        # l = sorted([(self.row_set[x], x) for x in rows])
        # print("============================")
        # print("============================")
        # print(rows)
        # print(l)

        # rows = []
        # for prio, x in l:
            # if prio < self.M:
                # rows.append(x)


        for clues, boundaries, transpose, the_rows, M, rs in [(self.rowclues, self.rowboundaries, False, rows, self.M, self.row_set), (self.colclues, self.colboundaries, True, cols, self.N, self.col_set)]:
            for x in the_rows:
                clue = clues[x]
                boundary = boundaries[x]

                if len(clue) == 0:
                    continue   # Nothing to learn

                line = str(sum(i * s for i, s in zip([self.get(x, i, transpose) for i in range(0, M)], threes)))
                line += '  -  ' + '.'.join(str(c) for c in clue)

                # print("==============", transpose, x)
                # self.print()


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


                # TODO: FIX

                # print("===========================")
                # print(clue)
                # print(boundary)
                # print(left)
                # print(right)


                # if left is not None and right is not None:
                    # boundaries[x] = [(l, r) for l, r in zip(left, right)]
                    # print("==================================")
                    # print("==================================")
                    # print(boundaries[x])


                    # print(boundaries[x])

                    # for i, (l, r) in enumerate(zip(left, right)):
                        # boundaries[x][i] = (l, r)

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


    # Actually worse than before, let's check if it's because it's buggy or a bad idea
    def next_guess(self):
        # row = 0
        # current = self.row_set[0] + sum(self.rowclues[0]) + len(self.rowclues[0])
        # for x in range(1, self.N):
            # if self.M > self.row_set[x] and self.row_set[x] + sum(self.rowclues[x]) + len(self.rowclues[x]) > current:
                # row = x
                # current = self.row_set[x] + sum(self.rowclues[x]) + len(self.rowclues[x])

        # col = None
        # for y in range(0, self.M):
            # if self.N > self.col_set[y] and self.col_set[y] + sum(self.colclues[y]) + len(self.colclues[y]) > current:
                # col = y
                # current = self.col_set[y] + sum(self.colclues[y]) + len(self.colclues[y])

        # if col:
            # for x in range(0, self.N):
                # if self.grid[x][col] == 2:
                    # return (x, col)
        # else:
            # for y in range(0, self.M):
                # if self.grid[row][y] == 2:
                    # return (row, y)

        # raise ValueError("EEEE")


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


    def guess(self):
        done = False
        for x in range(0, self.N):
            for y in range(0, self.M):
                if self.grid[x][y] == 2:
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



clues = (((25,), (1, 1), (1, 2, 1), (1, 3, 1), (1, 5, 1), (1, 5, 1), (1, 7, 1), (1, 7, 1), (1, 7, 1), (1, 7, 1), (1, 7, 1), (1, 6, 1), (1, 5, 1), (1, 4, 1), (1, 5, 1), (1, 7, 1), (1, 7, 1), (1, 9, 1), (1, 6, 3, 1), (1, 8, 2, 2, 1), (1, 2, 1, 2, 3, 1, 1), (1, 2, 2, 4, 1, 2), (1, 3, 4, 1, 1, 4), (2, 1, 1, 1, 1, 1, 1), (2, 2, 1, 1, 2, 1), (1, 2, 2, 2, 2, 1), (1, 1, 4, 2, 1), (1, 3, 4, 1), (1, 3, 6, 1), (1, 9, 1), (1, 8, 1), (1, 6, 1), (1, 3, 1), (1, 1), (25,)), ((35,), (1, 2, 1), (1, 1, 1, 1), (1, 1, 2, 1), (1, 4, 1), (1, 2, 1), (1, 5, 2, 1), (1, 9, 5, 1, 1), (1, 18, 2, 1, 1, 1), (1, 24, 2, 1), (1, 17, 1, 4, 1), (1, 16, 4, 1, 3, 1), (1, 6, 6, 1, 1, 2, 1), (1, 3, 5, 2, 4, 1), (1, 1, 2, 1, 4, 1), (1, 2, 3, 6, 1), (1, 1, 9, 1), (1, 2, 8, 1), (1, 2, 5, 1), (1, 1, 1), (1, 2, 1), (1, 1, 1, 1), (1, 2, 1, 1), (1, 2, 1), (35,)))



# clues = (((1, 1), (4,), (1, 1, 1), (3,), (1,)), ((1,), (2,), (3,), (2, 1), (4,)))


















start = time()

n = Nonogram(clues)

res = n.solve()

print(n.row_set)
print(n.col_set)

print("===================== RESULT")



# print(n.N, n.M)

# for x, c in enumerate(n.rowclues):
    # print(x, c)

# for o in n.order:
    # print(o)
# print(n.rowclues)
# print(n.order)

# print("===========================")
# while True:
    # o = heapq.heappop(n.order)
    # print(o)

t.print_events()


print(res)
# n.print()




print("==> Duration:", time() - start)



