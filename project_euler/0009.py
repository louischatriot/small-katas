import sys

N = 1000

for a in range(1,N+1):
    for b in range(a, N+1):
        c = N - a - b
        m = max(a, b, c)
        if m ** 2 == a * a + b * b + c * c - m * m:
            if a * b * c > 0:
                print(a * b * c)
                sys.exit(0)




