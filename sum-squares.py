from math import isqrt
from time import time


Nmax = 1001

squares = set(i * i for i in range(0, isqrt(2 * Nmax) + 1))
nexts = {p: [n for n in range(0, Nmax) if p + n in squares and p != n] for p in range(0, Nmax)}


