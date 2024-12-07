import math

def lcm(a, b):
    return a * b // math.gcd(a, b)

res = 1
for n in range(1, 21):
    res = lcm(res, n)

print(res)


