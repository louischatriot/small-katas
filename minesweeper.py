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



map = small_map
res = small_res
solution = [[int(c) if c != 'x' else 'x' for c in l.split(' ')] for l in res.split('\n')]
n_mines = sum([sum([1 if c == 'x' else 0 for c in l]) for l in solution])


deltas = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx != 0 or dy != 0]


def open(x, y):
    if solution is not None:
        if solution[x][y] == 'x':
            raise ValueError("Boom")
        else:
            return solution[x][y]







class Game():
    def __init__(self, map, n_mines):
        self.map = [[int(c) if c != '?' else '?' for c in l.split(' ')] for l in map.split('\n')]
        self.N, self.M = len(self.map), len(self.map[0])
        self.remaining_mines = n_mines

        self.todo_zeroes = list()
        self.todo_simple = list()
        self.todo_merge = list()

        # Assuming we never get anything else than zeroes as hints initially
        for x in range(0, self.N):
            for y in range(0, self.M):
                if self.map[x][y] == 0:
                    self.todo_zeroes.append((x, y))

    def print(self):
        print("=================================")
        print('\n'.join([' '.join([str(c) if str(c) != '?' else '.' for c in l]) for l in self.map]))


    def explore_zeroes(self):
        while len(self.todo_zeroes) > 0:
            x, y = self.todo_zeroes.pop(0)
            for dx, dy in deltas:
                if 0 <= x + dx < self.N and 0 <= y + dy < self.M:
                    if self.map[x + dx][y + dy] == '?':
                        v = open(x + dx, y + dy)
                        self.map[x + dx][y + dy] = v
                        if v == 0:
                            self.todo_zeroes.append((x + dx, y + dy))
                        else:
                            self.todo_simple.append((x + dx, y + dy))
                            # TODO: should we also add to the complex analysis? Probably yes


    def deduce_simple(self):
        while len(self.todo_simple) > 0:
            x, y = self.todo_simple.pop(0)
            v = self.map[x][y]

            # Touching the same number of cells as remaining neighbour mines
            opened = 0
            mines = 0
            for dx, dy in deltas:
                if 0 <= x + dx < self.N and 0 <= y + dy < self.M:
                    if self.map[x + dx][y + dy] == '?':
                        opened += 1
                    elif self.map[x + dx][y + dy] == 'x':
                        mines += 1

            if opened != 0 and opened + mines == v:
                for dx, dy in deltas:
                    if 0 <= x + dx < self.N and 0 <= y + dy < self.M:
                        if self.map[x + dx][y + dy] == '?':
                            self.map[x + dx][y + dy] = 'x'
                            self.remaining_mines -= 1


    def deduce(self):
        self.explore_zeroes()

        self.print()

        self.deduce_simple()



    def solve(self):
        self.deduce()

        # TODO: we will likely need some logic at the end of the game, based on the number of mines remaining





def solve_mine(map, n):
    game = Game(map, n)
    game.solve()













t.reset()

# solve_mine(map, n_mines)

game = Game(map, n_mines)
game.print()

game.deduce()
game.print()


t.time("Algo done")












