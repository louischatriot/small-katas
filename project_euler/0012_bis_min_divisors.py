import math

D = 500

# Get all lists of factors that verify:
# * Product is at least D
# * Length of list is equal to L
# * Factors are in decreasing order
# * Largest factor is D
def factors(L, D):
    if L == 1:
        yield [math.ceil(D)]
        return

    for f in range(math.ceil(D), 0, -1):
        rest = D / f

        for facts in factors(L-1, rest):
            if f >= facts[0]:
                yield [f] + facts


primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]  # Length l needs to verify 2^l >= D so need more primes if D bigger
res = 999999999999

for L in range(1, 10):
    for facts in factors(L, D):
        res = min(res, math.prod(a ** (b-1) for a, b in zip(primes, facts)))


print(res)


