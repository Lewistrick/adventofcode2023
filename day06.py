from math import sqrt

with open("06.example.in") as f:
    times = map(int, f.readline().removeprefix("Time:").strip().split())
    dists = map(int, f.readline().removeprefix("Distance:").strip().split())

games = [(t, d) for t, d in zip(times, dists)]

part1 = 1
for maxtime, record in games:
    ways2win = 0
    for speed in range(1, maxtime):
        dist = speed * (maxtime - speed)
        if dist > record:
            ways2win += 1
    part1 *= ways2win
print(part1)

# ---
# distance d is a function of time t
# where t goes from 0..m (m being max time)
# as seen above: d = s(m-s) where s = speed
# and speed is also a function of time: s = m - t

# d = s(m - s)
#   = -s^2 - m
#   = -(m-t)^2 - m
#   = -(m^2 - 2tm + t^2) - m
#   = -m^2 + 2tm - t^2 - m
#   = -t^2 + 2tm - m^2 - m

# now given d is a function of t and m being constant,
# we want to find the intersections with r, the record distance
# -t^2 + 2tm - m^2 - m = r
# -t^2 + 2tm - m^2 - m - r = 0

# we can solve this using the abc formula with
# a = -1
# b = 2m
# c = -m^2 - m - r
# D = b^2 - 4ac = (2m)^2 - 4 * -1 * (-m^2 - m - r)
# let's replace (-m^2 - m - r) with C
# D = 4m^2 - (-4 * C)
#   = 4m^2 + 4C = 4(m^2 + C)
# sqrt(D) = 2sqrt(m^2+C)

# d = (-b ± sqrt(D)) / 2a

# d1 = (-2m + 2sqrt(m^2+C)) / -2 = m - sqrt(m^2 + C)
# d2 = (-2m - 2sqrt(m^2+C)) / -2 = m + sqrt(m^2 + C)
# where
# sqrt(m^2 + C) = sqrt(m^2 - m^2 - m - r) = sqrt(m - r)
# so
# d1 = m - sqrt(m-r)
# d2 = m + sqrt(m-r)

times = [game[0] for game in games]
dists = [game[1] for game in games]

m = int("".join(map(str, times)))
r = int("".join(map(str, dists)))
print(m, r)


d1 = m - sqrt(m - r)
d2 = m + sqrt(m - r)
print(d1, d2)
