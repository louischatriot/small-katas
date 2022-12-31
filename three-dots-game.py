from time import time
import heapq

dirs = {'↑': (-1, 0),
        '↓': (1, 0),
        '←': (0, -1),
        '→': (0, 1)
        }

deltas = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if abs(dx ^ dy) == 1]


# Max distance between three sets of two points
def dist(a, b):
    return max(abs(a[0] - b[0]) + abs(a[1] - b[1]), abs(a[2] - b[2]) + abs(a[3] - b[3]), abs(a[4] - b[4]) + abs(a[5] - b[5]))


def bfs(map, cut = 999):
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
    to_do = []

    heapq.heappush(to_do, (0, start, ''))


    while len(to_do) > 0:
        priority, pos, path = heapq.heappop(to_do)

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

            if abs(new[0] - new[2]) + abs(new[1] - new[3]) <= cut and abs(new[4] - new[2]) + abs(new[5] - new[3]) <= cut and abs(new[0] - new[4]) + abs(new[1] - new[5]) <= cut:
                heapq.heappush(to_do, (dist(new, end), new, path + d))
                # to_do.append((new, path + d))

    return None



def three_dots(game_map):
    try:
        return bfs(game_map, 39999)
    except:
        return None





# map1 = "+------------+\n" + "|R    *******|\n" + "|G    *******|\n" + "|Y    *******|\n" + "|            |\n" + "|           r|\n" + "|******     g|\n" + "|******     y|\n" + "+------------+"

# print(map1)

# res = bfs(map1)

# print(res)



map2_better = (
  "+------------+\n"
+ "|R ** ***|\n"
+ "|G ** ***|\n"
+ "|Y       |\n"
+ "|        |\n"
+ "|        |\n"
+ "|        |\n"
+ "|       g|\n"
+ "|** *** r|\n"
+ "|** *** y|\n"
+ "+------------+")


# print(map2_better)



map2 =  "+------------+\n" + "|R     ** ***|\n" + "|G     ** ***|\n" + "|Y           |\n" + "|            |\n" + "|            |\n" + "|            |\n" + "|           g|\n" + "|** ***     r|\n" + "|** ***     y|\n" + "+------------+"

print(map2)

start = time()

res = three_dots(map2)

print(res)
print("==> Duration:", time() - start)







