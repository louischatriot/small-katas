from time import time

dirs = {'↑': (-1, 0),
        '↓': (1, 0),
        '←': (0, -1),
        '→': (0, 1)
        }

deltas = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if abs(dx ^ dy) == 1]



def bfs(map):
    walls = set()
    start = dict()
    end = dict()

    for x, line in enumerate(map.split('\n')):
        for y, c in enumerate(line):
            if c == ' ':
                pass
            elif c in ['R', 'G', 'Y']:
                start[c] = (x, y)
            elif c in ['r', 'g', 'y']:
                end[c] = (x, y)
            else:
                walls.add((x, y))

    start = (start['R'][0], start['R'][1], start['G'][0], start['G'][1], start['Y'][0], start['Y'][1])
    end = (end['r'][0], end['r'][1], end['g'][0], end['g'][1], end['y'][0], end['y'][1])

    paths = dict()
    to_do = [(start, '')]

    while True:
        pos, path = to_do.pop(0)

        if pos in paths:
            continue

        paths[pos] = path

        if pos == end:
            return path

        for d, delta in dirs.items():
            new = ()
            for p in [0, 1, 2]:
                x, y = pos[2 * p], pos[2 * p + 1]
                dx, dy = delta
                if (x + dx, y + dy) not in walls:
                    x += dx
                    y += dy

                new = new + (x, y)

            to_do.append((new, path + d))







map1 = "+------------+\n" + "|R    *******|\n" + "|G    *******|\n" + "|Y    *******|\n" + "|            |\n" + "|           r|\n" + "|******     g|\n" + "|******     y|\n" + "+------------+"

print(map1)


res = bfs(map1)


print(res)


