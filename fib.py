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



from math import isqrt

fibs = [0, 1]

f_max = 2000

for i in range(0, f_max):
    fibs.append(fibs[-1] + fibs[-2])

products = [fibs[i] * fibs[i+1] for i in range(0, len(fibs) -1)]


def productFib(prod):
    i = 0
    # Should really do a dichotomy ...
    while True:
        if products[i] < prod:
            i += 1
        else:
            break

    return [fibs[i], fibs[i+1], products[i] == prod]









