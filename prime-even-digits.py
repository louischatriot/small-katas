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


def n_even_digits(n):
    return sum(1 if int(d) % 2 == 0 else 0 for d in str(n))

primes = primes_until_n(m_max)

# primes_even_digits = [n_even_digits(p) for p in primes]



def f(n):
    res = primes[0]
    nd = n_even_digits(res)
    for p in primes:
        if p >= n:
            break
        else:
            ndc = n_even_digits(p)
            if ndc >= nd:
                nd = ndc
                res = p

    return res


