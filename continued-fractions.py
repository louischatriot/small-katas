from math import sqrt


def generate_continued_fraction(n):
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


res = generate_continued_fraction(1999 * 9001)

print(res)



