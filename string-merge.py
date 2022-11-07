
def is_merge(s, part1, part2):
    i1 = 0
    i2 = 0
    for i, l in enumerate(s):
        if i1 >= len(part1):
            return s[i:] == part2[i2:]

        if i2 >= len(part2):
            return s[i:] == part1[i1:]



        if part1[i1] == l:
            i1 += 1
        elif part2[i2] == l:
            i2 += 1
        else:
            return False

    return i1 == len(part1) and i2 == len(part2)



s = "Bananas from Bahamas"
p1 = "Bahas"
p2 = "Bananas from am"


# res = is_merge(s, p1, p2)

# print(res)




s = "codewars"
p1 = "code"
p2 = "wars"


res = is_merge(s, p1, p2)

print(res)




