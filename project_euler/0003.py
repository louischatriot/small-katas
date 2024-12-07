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
        primes = primes_until_n(math.floor(math.sqrt(n)) + 1)

    res = []

    for p in primes:
        if p > n:
            break

        while n % p == 0:
            res.append(p)
            n = n // p

    return res


factors = get_prime_factors(600851475143)
res = sorted(factors)[-1]

print(res)

