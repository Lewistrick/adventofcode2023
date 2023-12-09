data: list[list[int]] = []

with open("09.in") as lines:
    for line in lines:
        data.append(list(map(int, line.split())))


def extrapolate(row: list[list[int]], future=True):
    diffs: list[list[int]] = [row.copy()]
    while True:
        newrow = []
        for v1, v2 in zip(row[:-1], row[1:]):
            newrow.append(v2 - v1)

        diffs.append(newrow)
        if all(v == 0 for v in newrow):
            break

        row = newrow

    history: list[list[int]] = []
    currval = 0
    for r in diffs[::-1]:
        if future:
            currval += r[-1]
            history.append(r + [currval])
        else:
            currval = r[0] - currval
            history.append([currval] + r)

    return currval


part1 = 0
for row in data:
    newval = extrapolate(row.copy())
    part1 += newval

print(part1)

part2 = 0
for row in data:
    newval = extrapolate(row.copy(), future=False)
    part2 += newval

print(part2)
