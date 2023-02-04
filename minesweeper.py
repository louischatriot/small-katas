import time
class Timer():
    def __init__(self):
        self.reset()

    def reset(self):
        self.start = time.time()
        self.events = {}
        self.current_events = {}

    def time(self, message = ''):
        duration = time.time() - self.start
        print(f"{message} ===> Duration: {duration}")
        self.reset()

    def start_event(self, evt):
        self.current_events[evt] = time.time()

    def stop_event(self, evt):
        if evt not in self.events:
            self.events[evt] = (0, 0)

        self.events[evt] = (self.events[evt][0] + time.time() - self.current_events[evt], self.events[evt][1] + 1)


    def print_events(self):
        for evt, v in self.events.items():
            print(f"{evt} - avg {v[0] / v[1]} - total {v[0]} - number {v[1]}")


t = Timer()


big_map = """
? ? 0 ? ? ? 0 0 ? ? ? 0 0 0 0 ? ? ? 0
? ? 0 ? ? ? 0 0 ? ? ? 0 0 0 0 ? ? ? ?
? ? 0 ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? ?
0 ? ? ? ? ? ? ? ? ? ? 0 0 0 0 0 ? ? ?
0 ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 0 0
0 ? ? ? 0 0 0 ? ? ? 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 ? ? ? ? ? ? ? 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 ? ? ? ? 0 0 0 0 0
0 0 ? ? ? 0 ? ? ? 0 ? ? ? ? 0 0 0 0 0
0 0 ? ? ? ? ? ? ? 0 0 0 0 0 0 ? ? ? 0
0 0 ? ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? 0
0 0 0 0 ? ? ? ? ? ? ? 0 0 0 0 ? ? ? 0
0 0 0 0 0 ? ? ? ? ? ? 0 0 0 0 0 ? ? ?
0 0 ? ? ? ? ? ? 0 0 0 0 0 0 0 0 ? ? ?
0 0 ? ? ? ? ? ? ? 0 0 0 0 0 0 0 ? ? ?
0 0 ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 ? ?
0 0 0 0 0 0 ? ? ? ? 0 0 0 ? ? ? 0 ? ?
0 0 0 ? ? ? ? ? ? ? 0 0 0 ? ? ? ? ? ?
0 0 0 ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ? ?
0 0 0 ? ? ? ? ? 0 0 0 ? ? ? 0 ? ? ? ?
0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
""".strip()


big_res = """
1 1 0 1 1 1 0 0 1 1 1 0 0 0 0 1 1 1 0
x 1 0 1 x 1 0 0 2 x 2 0 0 0 0 1 x 2 1
1 1 0 2 3 3 1 1 3 x 2 0 0 0 0 1 2 x 1
0 1 1 2 x x 1 2 x 3 1 0 0 0 0 0 1 1 1
0 1 x 2 2 2 1 3 x 3 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 2 x 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 1 2 2 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 x x 1 0 0 0 0 0
0 0 1 1 1 0 1 1 1 0 1 2 2 1 0 0 0 0 0
0 0 1 x 2 1 3 x 2 0 0 0 0 0 0 1 1 1 0
0 0 1 1 2 x 3 x 3 1 1 0 0 0 0 1 x 1 0
0 0 0 0 1 2 3 2 2 x 1 0 0 0 0 1 1 1 0
0 0 0 0 0 1 x 1 1 1 1 0 0 0 0 0 1 1 1
0 0 1 1 2 2 2 1 0 0 0 0 0 0 0 0 1 x 1
0 0 1 x 2 x 2 1 1 0 0 0 0 0 0 0 1 1 1
0 0 1 1 2 1 3 x 3 1 0 0 0 0 0 0 0 1 1
0 0 0 0 0 0 2 x x 1 0 0 0 1 1 1 0 1 x
0 0 0 1 1 1 1 2 2 1 0 0 0 1 x 1 1 2 2
0 0 0 1 x 3 2 1 0 0 0 1 1 2 1 1 1 x 2
0 0 0 1 2 x x 1 0 0 0 1 x 1 0 1 2 3 x
0 0 0 0 1 2 2 1 1 1 1 1 1 1 0 1 x 3 2
0 0 0 0 1 1 1 1 2 x 1 1 1 1 0 2 3 x 2
0 0 0 0 1 x 1 1 x 2 1 1 x 1 0 1 x 3 x
""".strip()


small_map = """
? ? ? ? ? ?
? ? ? ? ? ?
? ? ? 0 ? ?
? ? ? ? ? ?
? ? ? ? ? ?
0 0 0 ? ? ?
""".strip()


small_res = """
1 x 1 1 x 1
2 2 2 1 2 2
2 x 2 0 1 x
2 x 2 1 2 2
1 1 1 1 x 1
0 0 0 1 1 1
""".strip()



rectangle_map = """
0 0 0 0 0 0 0 0 ? ? ? ? ? 0 ? ? ? 0 ? ? ?
0 0 0 0 0 0 0 0 ? ? ? ? ? 0 ? ? ? ? ? ? ?
0 0 0 0 0 0 0 0 0 0 ? ? ? 0 ? ? ? ? ? ? ?
0 0 0 0 0 ? ? ? 0 0 ? ? ? 0 ? ? ? ? ? ? 0
? ? 0 0 0 ? ? ? 0 ? ? ? ? 0 0 ? ? ? ? ? ?
? ? 0 0 0 ? ? ? 0 ? ? ? 0 0 0 ? ? ? ? ? ?
? ? ? 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 ? ? ?
? ? ? 0 0 0 0 0 0 0 ? ? ? ? 0 0 ? ? ? 0 0
? ? ? 0 0 0 0 0 0 0 ? ? ? ? 0 0 ? ? ? 0 0
""".strip()

rectangle_res = """
0 0 0 0 0 0 0 0 1 x x 2 1 0 1 x 1 0 1 2 x
0 0 0 0 0 0 0 0 1 2 3 x 1 0 2 2 2 1 2 x 2
0 0 0 0 0 0 0 0 0 0 2 2 2 0 1 x 1 1 x 2 1
0 0 0 0 0 1 1 1 0 0 1 x 1 0 1 2 2 2 1 1 0
1 1 0 0 0 1 x 1 0 1 2 2 1 0 0 1 x 1 1 1 1
x 1 0 0 0 1 1 1 0 1 x 1 0 0 0 1 1 1 1 x 1
2 2 1 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 1 1 1
1 x 1 0 0 0 0 0 0 0 1 2 2 1 0 0 1 1 1 0 0
1 1 1 0 0 0 0 0 0 0 1 x x 1 0 0 1 x 1 0 0
""".strip()



map1 = """
0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 0 0 ? ? ? ? ? ? 0
0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? 0 ? ? ? 0 0 0 0 ? ? ? ? ? ? 0
? ? ? 0 0 0 0 ? ? ? 0 0 0 0 ? ? ? ? ? 0 0 0 0 ? ? ? ? ? ? 0
? ? ? ? ? ? 0 ? ? ? ? ? 0 0 ? ? ? ? ? 0 0 0 0 ? ? ? 0 0 0 0
? ? ? ? ? ? 0 ? ? ? ? ? 0 0 ? ? ? ? 0 0 0 0 0 ? ? ? 0 0 ? ?
0 ? ? ? ? ? 0 0 0 ? ? ? 0 ? ? ? ? ? 0 0 0 0 0 ? ? ? 0 0 ? ?
0 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ?
0 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? 0 ? ? ? 0 0 ? ? ? 0
0 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? 0 ? ? ? 0 0 ? ? ? 0
? ? ? ? 0 ? ? ? ? 0 0 0 ? ? ? ? ? ? ? 0 0 ? ? ? 0 0 ? ? ? 0
? ? ? ? 0 ? ? ? ? ? 0 0 ? ? ? ? ? ? ? 0 0 0 ? ? ? 0 0 0 0 0
? ? ? ? ? ? ? ? ? ? 0 0 ? ? ? ? ? ? ? 0 0 0 ? ? ? ? 0 0 0 0
? ? ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? ? ? 0 0 0 ? ? ? ? 0 0 0 0
? ? ? ? ? ? ? 0 0 ? ? ? 0 0 ? ? ? 0 0 0 0 0 ? ? ? ? 0 0 0 0
? ? ? ? 0 0 0 0 0 ? ? ? 0 0 ? ? ? 0 0 0 0 0 ? ? ? 0 0 0 0 0
""".strip()


res1 = """
0 0 0 0 0 0 0 0 0 0 0 0 1 x 1 0 0 0 0 0 0 0 0 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 1 1 1 0 0 0 0 2 x 2 1 x 1 0
1 1 1 0 0 0 0 1 1 1 0 0 0 0 1 1 2 x 1 0 0 0 0 2 x 2 1 1 1 0
1 x 1 1 1 1 0 1 x 2 1 1 0 0 1 x 2 1 1 0 0 0 0 1 1 1 0 0 0 0
1 2 2 3 x 2 0 1 1 2 x 1 0 0 1 2 2 1 0 0 0 0 0 1 1 1 0 0 1 1
0 1 x 3 x 2 0 0 0 1 1 1 0 1 2 3 x 1 0 0 0 0 0 1 x 1 0 0 1 x
0 1 1 3 3 3 2 1 1 1 1 2 1 2 x x 2 2 1 1 0 0 0 1 1 1 1 1 2 1
0 0 0 1 x x 2 x 1 1 x 2 x 2 3 3 3 2 x 1 0 1 1 1 0 0 2 x 2 0
0 1 1 2 2 2 3 2 2 1 1 2 1 1 1 x 2 x 2 1 0 1 x 1 0 0 2 x 2 0
1 2 x 1 0 1 2 x 1 0 0 0 1 1 2 2 3 2 1 0 0 1 1 1 0 0 1 1 1 0
1 x 2 1 0 1 x 3 2 1 0 0 1 x 1 1 x 2 1 0 0 0 1 1 1 0 0 0 0 0
1 1 2 1 2 2 2 2 x 1 0 0 1 1 1 1 2 x 1 0 0 0 1 x 2 1 0 0 0 0
1 1 2 x 2 x 1 1 1 1 0 0 0 0 1 1 2 1 1 0 0 0 1 2 x 1 0 0 0 0
1 x 3 2 2 1 1 0 0 1 1 1 0 0 1 x 1 0 0 0 0 0 1 2 2 1 0 0 0 0
1 2 x 1 0 0 0 0 0 1 x 1 0 0 1 1 1 0 0 0 0 0 1 x 1 0 0 0 0 0
""".strip()




map = map1
res = res1
solution = [[int(c) if c != 'x' else 'x' for c in l.split(' ')] for l in res.split('\n')]
n_mines = sum([sum([1 if c == 'x' else 0 for c in l]) for l in solution])


def open(x, y):
    if solution is not None:
        if solution[x][y] == 'x':
            raise ValueError("Boom")
        else:
            return solution[x][y]

# Code for Codewars below this



full_deltas = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1]]
deltas = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx != 0 or dy != 0]



# Each 3x3 square represented by a unique number whose binary representation says
# where there are mines
# e.g. 105 is 0b001101001 meaning 0 0 1
#                                 1 0 1
#                                 0 0 1  --> center touches 4 mines
squares = [i for i in range(0, 2**9)]
np = len(squares)

def rep(n):
    msg = str(bin(n))[2:]
    while len(msg) < 9:
        msg = '0' + msg
    msg = ''.join(['.' if c == '0' else 'x' for c in msg])
    msg = msg[0:3] + '\n' + msg[3:6] + '\n' + msg[6:9]
    return msg

def print_square(n):
    print('---------')
    print(rep(n))
    print('---------')

def mines_in(n):
    return sum([1 if d == '1' else 0 for d in bin(n)])

def is_cell_mine(n, x, y):
    mask = 2 ** (8 - 3 * x - y)
    return mask & n > 0

def print_path(p):
    msgs = []

    for n in p:
        msg = str(bin(n))[2:]
        while len(msg) < 9:
            msg = '0' + msg
        msg = ''.join(['.' if c == '0' else 'x' for c in msg])
        msgs.append(msg)


    res = ''
    for i in range(0, 3):
        line = msgs[0][3 * i:3 * (i+1)] + ''.join([msgs[m][3 * (i+1) - 1] for m in range(1, len(msgs))])
        res += line + '\n'

    # res = '\n'.join(['   '.join([msg[3 * i:3 * (i+1)] for msg in msgs]) for i in range(0, 3)])
    print('--------------------------------------------------------------------------')
    print(res)
    print('--------------------------------------------------------------------------')


next_r = [set([((i & 0b011011011) << 1) + o1 * 0b001000000 + o2 * 0b000001000 + o3 * 0b000000001 for o1 in [0, 1] for o2 in [0, 1] for o3 in [0, 1]]) for i in range(0, np)]
next_b = [set([((i & 0b000111111) << 3) + o for o in range(0, 8)]) for i in range(0, np) ]


# Should refact just because this is really ugly
center_mine = 0b10000
east_mines = 0b001001001
west_mines = 0b100100100
north_mines = 0b111000000
south_mines = 0b000000111
nw_mines = 0b111100100
ne_mines = 0b111001001
sw_mines = 0b100100111
se_mines = 0b001001111

center = dict()
east = dict()
west = dict()
north = dict()
south = dict()
nw = dict()
ne = dict()
sw = dict()
se = dict()

center['x'] = set()
east['x'] = set()
west['x'] = set()
north['x'] = set()
south['x'] = set()
nw['x'] = set()
ne['x'] = set()
sw['x'] = set()
se['x'] = set()

for n in range(0, np):
    if n & center_mine == 0:
        nm = mines_in(n)
        if nm not in center:
            center[nm] = set()
            west[nm] = set()
            east[nm] = set()
            north[nm] = set()
            south[nm] = set()
            nw[nm] = set()
            ne[nm] = set()
            sw[nm] = set()
            se[nm] = set()

        center[nm].add(n)
        if n & west_mines == 0:
            west[nm].add(n)
        if n & east_mines == 0:
            east[nm].add(n)
        if n & north_mines == 0:
            north[nm].add(n)
        if n & south_mines == 0:
            south[nm].add(n)

        if n & nw_mines == 0:
            nw[nm].add(n)
        if n & ne_mines == 0:
            ne[nm].add(n)
        if n & sw_mines == 0:
            sw[nm].add(n)
        if n & se_mines == 0:
            se[nm].add(n)

    else:
        center['x'].add(n)
        if n & west_mines == 0:
            west['x'].add(n)
        if n & east_mines == 0:
            east['x'].add(n)
        if n & north_mines == 0:
            north['x'].add(n)
        if n & south_mines == 0:
            south['x'].add(n)

        if n & nw_mines == 0:
            nw['x'].add(n)
        if n & ne_mines == 0:
            ne['x'].add(n)
        if n & sw_mines == 0:
            sw['x'].add(n)
        if n & se_mines == 0:
            se['x'].add(n)








class Game():
    def __init__(self, map, n_mines):
        self.map = [[int(c) if c != '?' else '?' for c in l.split(' ')] for l in map.split('\n')]
        self.N, self.M = len(self.map), len(self.map[0])
        self.remaining_mines = n_mines

        self.todo_zeroes = set()
        self.todo_simple = set()
        self.todo_merge = set()

        # TODO: checking off strategy is very basic and could make the algorithm much faster
        self.fully_done = set()
        self.opened = set()

        # Assuming we never get anything else than zeroes as hints initially
        for x in range(0, self.N):
            for y in range(0, self.M):
                if self.map[x][y] == 0:
                    self.todo_zeroes.add((x, y))
                    self.opened.add((x, y))

        # For the merging
        self.square_types = [[center for _ in range(0, self.M)] for _ in range(0, self.N)]
        for x in range(1, self.N - 1):
            self.square_types[x][-1] = east
            self.square_types[x][0] = west
        for y in range(1, self.M - 1):
            self.square_types[-1][y] = south
            self.square_types[0][y] = north
        self.square_types[0][0] = nw
        self.square_types[0][-1] = ne
        self.square_types[-1][0] = sw
        self.square_types[-1][-1] = se


    def print(self):
        print("=================================")
        print(self.string_rep())


    def string_rep(self):
        return '\n'.join([' '.join([str(c) if str(c) != '?' else '.' for c in l]) for l in self.map])


    def explore_zeroes(self):
        while len(self.todo_zeroes) > 0:
            x, y = self.todo_zeroes.pop()

            self.fully_done.add((x, y))

            for dx, dy in deltas:
                if 0 <= x + dx < self.N and 0 <= y + dy < self.M:
                    if self.map[x + dx][y + dy] == '?':
                        # Not using open_cell here
                        v = open(x + dx, y + dy)
                        self.map[x + dx][y + dy] = v
                        self.opened.add((x + dx, y + dy))
                        if v == 0:
                            self.todo_zeroes.add((x + dx, y + dy))
                        else:
                            self.todo_simple.add((x + dx, y + dy))


    # Add every neighbour of this newly uncovered mine to the list
    def add_neighbours(self, x, y):
        for dx, dy in deltas:
            nx, ny = x + dx, y + dy

            if 0 <= nx < self.N and 0 <= ny < self.M:
                if self.map[nx][ny] != '?' and (nx, ny) not in self.fully_done:
                    self.todo_simple.add((nx, ny))


    def mark_mine(self, x, y):
        if self.map[x][y] == 'x':
            return False
        elif self.map[x][y] == '?':
            self.map[x][y] = 'x'
            self.remaining_mines -= 1
            self.opened.add((x, y))
            self.add_neighbours(x, y)
            return True
        else:
            raise ValueError("What the heck")


    def open_cell(self, x, y):
        v = open(x, y)

        if self.map[x][y] == v:
            return False
        elif self.map[x][y] == '?':
            self.map[x][y] = v
            self.opened.add((x, y))

            if v == 0:
                self.todo_zeroes.add((x, y))
                self.explore_zeroes()
            else:
                self.todo_simple.add((x, y))
                self.add_neighbours(x, y)

            return True
        else:
            raise ValueError("What the fuck")


    def deduce_simple(self):
        while len(self.todo_simple) > 0:
            x, y = self.todo_simple.pop()

            if (x, y) in self.fully_done:
                continue

            v = self.map[x][y]

            # Touching the same number of cells as remaining neighbour mines
            unopened = 0
            mines = 0
            for dx, dy in deltas:
                if 0 <= x + dx < self.N and 0 <= y + dy < self.M:
                    if self.map[x + dx][y + dy] == '?':
                        unopened += 1
                    elif self.map[x + dx][y + dy] == 'x':
                        mines += 1

            # All squares touching this one are mines
            if unopened != 0 and unopened + mines == v:
                for dx, dy in deltas:
                    if 0 <= x + dx < self.N and 0 <= y + dy < self.M:
                        if self.map[x + dx][y + dy] == '?':
                            self.mark_mine(x + dx, y + dy)

                self.fully_done.add((x, y))

                continue

            # All squares touching this one are empty
            if unopened != 0 and mines == v:
                for dx, dy in deltas:
                    if 0 <= x + dx < self.N and 0 <= y + dy < self.M:
                        if self.map[x + dx][y + dy] == '?':
                            self.open_cell(x + dx, y + dy)

                self.fully_done.add((x, y))

                continue

            # Could not make a simple deduction, adding to merge deductions list
            self.todo_merge.add((x, y))


    def mine_pattern(self, x, y):
        mines = 0
        unopened = 2 ** 9 - 1
        for dx, dy in full_deltas:
            if 0 <= x + dx < self.N and 0 <= y + dy < self.M:
                if self.map[x + dx][y + dy] == 'x':
                    mines += 2 ** (8 - 3 * (dx + 1) - (dy + 1))
                elif self.map[x + dx][y + dy] == '?':
                    unopened -= 2 ** (8 - 3 * (dx + 1) - (dy + 1))

        return mines, unopened


    def clean_todo_merge(self, scope=None):
        to_remove = set()

        to_look = self.todo_merge if scope is None else scope.intersection(self.todo_merge)
        for x, y in to_look:
            if (x, y) in self.fully_done:
                to_remove.add((x, y))
                continue

            # We may still get fully done squares here, if done through another square
            unopened = 0
            for dx, dy in deltas:
                if 0 <= x + dx < self.N and 0 <= y + dy < self.M:
                    if self.map[x + dx][y + dy] == '?':
                        unopened += 1

            if unopened == 0:
                self.fully_done.add((x, y))
                to_remove.add((x, y))
                continue


        for x, y in to_remove:
            self.todo_merge.remove((x, y))


    def deduce_merge(self):
        found_something = False

        for x, y in self.todo_merge:
            line_u = [(x, y)]
            line_d = [(x, y)]

            column_l = [(x, y)]
            column_r = [(x, y)]

            # Ugly code
            if x > 0:
                line_u = [(x, y)]

                for yp in range(y-1, -1, -1):
                    if (x, yp) in self.todo_merge and self.map[x-1][yp] == '?':
                        # Not optimal
                        line_u.insert(0, (x, yp))
                    else:
                        break

                for yp in range(y+1, self.M):
                    if (x, yp) in self.todo_merge and self.map[x-1][yp] == '?':
                        line_u.append((x, yp))
                    else:
                        break

            if x < self.N - 1:
                line_d = [(x, y)]

                for yp in range(y-1, -1, -1):
                    if (x, yp) in self.todo_merge and self.map[x+1][yp] == '?':
                        # Not optimal
                        line_d.insert(0, (x, yp))
                    else:
                        break

                for yp in range(y+1, self.M):
                    if (x, yp) in self.todo_merge and self.map[x+1][yp] == '?':
                        line_d.append((x, yp))
                    else:
                        break


            if max(len(line_u), len(line_d)) < 3:
                # So not optimal as well
                continue

            line = line_u if len(line_u) > len(line_d) else line_d
            ox, oy = (0, 1) if len(line_u) > len(line_d) else (2, 1)


            # TODO: do the column, then understand which one is the best boundary
            path = line


            # TODO: very inefficient, should keep track of the patterns we can't do anymore
            found_something = self.deduce_path(path, ox, oy)
            if found_something is True:
                break

        # We changed something,update todo merge and try to resume simple guesses
        if found_something:
            self.clean_todo_merge()   # Inefficient, should clean the path and its neighbours

        return found_something


    def deduce_path(self, path, ox, oy):
        zx, zy = path[1][0] - path[0][0], path[1][1] - path[0][1]

        if zx == 0:
            next_squares = next_r
            moving_coord = 1
        elif zy == 0:
            next_squares = next_b
            moving_coord = 0

        pos = [[]]
        for x, y in path:
            next = set()
            cells = self.square_types[x][y][self.map[x][y]]
            mines, unopened = self.mine_pattern(x, y)
            for n in cells:
                if unopened & n == mines:
                    next.add(n)

            _pos = []
            for p in pos:
                inter = next_squares[p[-1]].intersection(next) if len(p) > 0 else next

                for i in inter:
                    _pos.append(p + [i])

            pos = _pos

        # Range tracks both real and path coordinates
        the_range = [(i, ox, oy) for i in range(0, len(path))]
        if path[0][moving_coord] > 0:
            e = (0, ox - (1 if moving_coord == 0 else 0), oy - (1 if moving_coord == 1 else 0))
            the_range.insert(0, e)
        if path[-1][moving_coord] < self.M - 1:
            e = (len(path) - 1, ox + (1 if moving_coord == 0 else 0), oy + (1 if moving_coord == 1 else 0))
            the_range.append(e)

        # Not really beautiful to put unnecessary data
        mines = [(-1, -1, -1) for i in range(0, len(the_range))]   # -1 means never set, 2 means conflict

        for p in pos:
            for n, (i, _ox, _oy) in enumerate(the_range):
                v = 1 if is_cell_mine(p[i], _ox, _oy) else 0

                if mines[n][0] == -1:
                    mines[n] = (v, path[i][0] - 1 +_ox, path[i][1] - 1 + _oy)
                else:
                    if mines[n][0] != v:
                        mines[n] = (2, -1, -1)

        found_something = False
        for v, x, y in mines:
            if v != 2:
                found_something = True
                if v == 1:
                    self.mark_mine(x, y)
                else:
                    self.open_cell(x, y)

        return found_something


    def solve(self):
        self.explore_zeroes()

        # self.mark_mine(0, 19)

        while True:
            before = len(self.opened)

            self.deduce_simple()
            self.clean_todo_merge()
            self.deduce_merge()

            if self.remaining_mines == 0 or len(self.opened) == before:
                break

        self.print()


        if self.remaining_mines == 0:
            return self.string_rep()


        # Test all possibilities (??)
        # Assume that we don't need to do that for now and see if all cases are taken into account
        return '?'








def solve_mine(map, n):
    game = Game(map, n)
    return game.solve()













t.reset()

res = solve_mine(map, n_mines)

print(res)

1/0



game = Game(map, n_mines)
game.print()

game.deduce()
game.print()
print(game.remaining_mines)


t.time("Algo done")












