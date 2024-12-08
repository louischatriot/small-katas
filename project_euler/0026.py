N = 1000

def get_cycle_length(n):
    r = N % n  # Ugly but makes it easier ; assumes N is a power of 10

    pos = dict()
    c = 0
    while True:
        c += 1
        r = (r * 10) % n

        if c >= 2000:
            if r in pos:
                return c - pos[r]
            else:
                pos[r] = c


longest = 0
for n in range(1, N):
    longest = max(longest, get_cycle_length(n))

for n in range(1, N):
    if longest == get_cycle_length(n):
        print(n)


