def chk(a):
    d = {}
    for x in a:
        while (x > 0):
            p = x % 10
            if d.get(p) is None:
                d[p] = 1
            x = x // 10
    return len(d) == 10

n = int(input())

for _ in range(n):
    resh = []

    t = int(input())
    data = list(map(int, input().split()))

    f = False
    for i in range(t - 3):
        for j in range(i + 1, t - 2):
            for k in range(j + 1, t):
                if chk([data[i], data[j], data[k]]):
                    print(data[i], data[j], data[k])
                    f = True
                    break
            if f:
                break
        if f:
            break