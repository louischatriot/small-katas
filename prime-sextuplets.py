from math import isqrt, floor, gcd
import numpy


m_max = 5000000

def primes_until_n(n):
    n += 1
    sieve = numpy.ones(n//2, dtype=bool)
    for i in range(3,int(n**0.5)+1,2):
        if sieve[i//2]:
            sieve[i*i//2::i] = False
    return [2] + list(2*numpy.nonzero(sieve)[0][1::]+1)

primes = primes_until_n(m_max)

checks = {i: True for i in primes}

primes_sextuplets = [i for i in primes if i+4 in checks and i+6 in checks and i+10 in checks and i+12 in checks and i+16 in checks]

def find_primes_sextuplet(n):
    for i in primes_sextuplets:
        if 6 * i + 48 >= n:
            return [i, i+4, i+6, i+10, i+12, i+16]
