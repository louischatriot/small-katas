import numpy

def primes_until_n(n):
    n += 1
    sieve = numpy.ones(n//2, dtype=bool)
    for i in range(3,int(n**0.5)+1,2):
        if sieve[i//2]:
            sieve[i*i//2::i] = False
    return [2] + list(2*numpy.nonzero(sieve)[0][1::]+1)


primes = primes_until_n(1000000)  # Arbitrary to get enough primes, this is fast anyway

print(primes[10000])

