a=154476802108746166441951315019919837485664325669565431700026634898253202035277999
b=36875131794129999827197811565225474825492979968971970996283137471637224634055579
c=4373612677928697257861252602371390152816537558161613618621437993378423467772036

res = a / (b+c) + b/(a+c) + c/(a+b)
print(res)

res =  b/(a+c)
print(res)

res = a / (b+c)
print(res)

res =  c/(a+b)
print(res)



N = 10000
epsilon = 1e-8

for a in range(1, N):
    for b in range(1, N):
        for c in range(1, N):
            t = a / (b + c) + b / (a + c) + c / (a + b)

            if 4 - epsilon < t < 4 + epsilon:
                print("==================")
                print(t)
                print(a, b, c)

