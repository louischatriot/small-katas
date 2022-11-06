import time
class Timer():
    def __init__(self):
        self.reset()

    def reset(self):
        self.start = time.time()

    def time(self, message = ''):
        duration = time.time() - self.start
        print(f"{message} ===> Duration: {duration}")
        self.reset()

t = Timer()





from math import sqrt, isqrt


# Does not work because of compounding errors
def generate_continued_fraction_float(n):
    n = sqrt(n)

    a0 = int(n)
    res = [a0]

    current = a0
    for i in range(0, 15):
        n = 1 / (n - current)
        current = int(n)
        res.append(current)
        if current == 2 * a0:
            break

    return res



def generate_continued_fraction(n):
    if isqrt(n) ** 2 == n:
        def gen():
            yield isqrt(n)
            while True:
                yield 0

        return gen()


    def gen():
        a0 = isqrt(n)
        c = a0
        b = 1

        yield a0

        while True:
            d = (n - c ** 2) // b

            a = (a0 + c) // d
            while (a + 1) * d <= a0 + c:
                a += 1

            yield a

            c = a * d - c
            b = d

    return gen()



# res = generate_continued_fraction(1999 * 9001)
# res = generate_continued_fraction(139)
# res = generate_continued_fraction(4012009)


u = 179769319999

t.reset()
res = generate_continued_fraction(u)
t.time("YO")



print(next(res))
print(next(res))
print(next(res))
print(next(res))
print(next(res))
print(next(res))
print(next(res))
print(next(res))
print(next(res))
print(next(res))
print(next(res))
print(next(res))
print(next(res))
print(next(res))




