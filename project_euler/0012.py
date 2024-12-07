from collections import defaultdict
import numpy
import math


def primes_until_n(n):
    n += 1
    sieve = numpy.ones(n//2, dtype=bool)
    for i in range(3,int(n**0.5)+1,2):
        if sieve[i//2]:
            sieve[i*i//2::i] = False
    return [2] + list(2*numpy.nonzero(sieve)[0][1::]+1)


def get_prime_factors(n, primes = None):
    if primes is None:
        primes = primes_until_n(n // 2 + 1)

    res = []

    for p in primes:
        if p > n:
            break

        while n % p == 0:
            res.append(p)
            n = n // p

    return res


def get_number_of_divisors(n, primes = None):
    pfs = get_prime_factors(n, primes)
    pfs_freq = defaultdict(lambda: 0)
    for pf in pfs:
        pfs_freq[pf] += 1

    return math.prod(n + 1 for n in pfs_freq.values())



primes = primes_until_n(100000000)
target = 500

for n in range(2, 1000000):
    s = n * (n + 1) // 2
    if get_number_of_divisors(s, primes) > target:
        print(s)
        1/0







