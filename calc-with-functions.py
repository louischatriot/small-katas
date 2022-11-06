def gen_number(n):
    def t(i = None):
        if i is None:
            return n
        else:
            m = i[0]
            if i[1] == "+":
                return n+m
            if i[1] == "-":
                return n-m
            if i[1] == "*":
                return n*m
            if i[1] == "//":
                return n//m

    return t

def gen_op(op):
    def t(n):
        return (n, op)

    return t

zero = gen_number(0)
one = gen_number(1)
two = gen_number(2)
three = gen_number(3)
four = gen_number(4)
five = gen_number(5)
six = gen_number(6)
seven = gen_number(7)
eight = gen_number(8)
nine = gen_number(9)

plus = gen_op('+')
minus = gen_op('-')
times = gen_op('*')
divided_by = gen_op('//')



