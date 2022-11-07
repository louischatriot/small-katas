def possibilities(s):
    buckets = []

    current = ''
    for i in s:
        if i != '?':
            current += i
        else:
            if len(current) > 0:
                buckets.append(current)
                current = ""
            buckets.append('?')

    if len(current) != 0:
        buckets.append(current)

    res = [""]

    for b in buckets:
        if b == '?':
            res = [i + '0' for i in res] + [i + '1' for i in res]
        else:
            res = [i + b for i in res]

    return res




res = possibilities('?01?110')
