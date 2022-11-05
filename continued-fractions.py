from math import sqrt


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
    sq = sqrt(n)

    a0 = int(sq)
    res = [a0]
    c = a0
    b = 1

    while True:
        d = (n - c ** 2) // b
        omega = (sq + c) / d
        a = int(omega)
        res.append(a)

        if a == 2 * a0:
            break

        c = a * d - c
        b = d

    return res



res = generate_continued_fraction(1999 * 9001)
# res = generate_continued_fraction(139)

print(res)



