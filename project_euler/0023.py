import numpy
import itertools
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


# Would be much more efficient to use a Erathostène's sieve like approach to calculate many of those sums
# See 2015 day 20
def sum_of_divisors(n, primes = None):
    prime_factors = get_prime_factors(n, primes)

    res = set()

    for L in range(len(prime_factors) + 1):
        for subset in itertools.combinations(prime_factors, L):
            res.add(math.prod(subset))

    return sum(res)



N = 10000
B = 28125
primes = primes_until_n(B)
proper_divisors = {n: sum_of_divisors(n, primes) - n for n in range(1, B)}
abundants = set()
ablist = list()
for n, s in proper_divisors.items():
    if s > n:
        abundants.add(n)
        ablist.append(n)

res = 0
for n in range(1, B):
    if not any((n-a) in abundants for a in ablist if a < n):
        res += n

print(res)


