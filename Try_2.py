
def prob(data):
    sets = 37
    if (data[5]+data[6]) > data[0]:
        return 0
    P_pete = (data[2] - data[1] + 1) / sets
    P_vasya = (data[4] - data[3] + 1) / sets
    print(P_pete, P_vasya)
    if data[2] < data[3]:
        P_none = 1 - P_pete - P_vasya
        print(P_none)
    elif data[2] > data[3]:
        P_none = 1 - (max(data[1:4]) - min(data[1:4]) + 1) / sets
        print(P_none)
    P = (P_pete ** (data[5])) * (P_vasya ** (data[6])) * (P_none) ** (data[0] - (data[5] + data[6]))

    return P

t = int(input())
for _ in range(t):
    data = list(map(int, input().split(" ")))
    print(prob(data))
