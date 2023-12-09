data: list[list[int]] = []

with open("09.in") as lines:
    for line in lines:
        data.append(list(map(int, line.split())))


def extrapolate(row: list[list[int]], future=True):
    diffs: list[list[int]] = [row.copy()]
    while True:
        diffrow = [v2 - v1 for v1, v2 in zip(row[:-1], row[1:])]
        diffs.append(diffrow)
        if all(v == 0 for v in diffrow):
            break

        row = diffrow

    diffrows: list[list[int]] = []
    currval = 0
    for r in diffs[::-1]:
        if future:
            currval += r[-1]
            diffrows.append(r + [currval])
        else:
            currval = r[0] - currval
            diffrows.append([currval] + r)

    return currval


part1 = sum(extrapolate(row.copy()) for row in data)
print(part1)

part2 = sum(extrapolate(row.copy(), future=False) for row in data)
print(part2)
