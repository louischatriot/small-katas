import itertools

# Ugly version
def is_palindrome(n):
    s = str(n)
    r = ''.join(list(reversed(s)))
    return r == s

res = -1
for i, j in itertools.product(range(1000), range(1000)):
    n = i * j
    if is_palindrome(n) and n > res:
        res = n

print(res)



