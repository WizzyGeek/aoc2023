
def calc_dist(time, held):
    return max(held * (time - held), 0)

def ways(time, dist):
    return sum(calc_dist(time, i) > dist for i in range(time + 1))

t = [49877895]
d = [356137815021882]

p = 1
for i in range(1):
    p *= ways(t[i], d[i])

print(p)