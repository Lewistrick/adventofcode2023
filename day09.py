data: list[list[int]] = []

with open("09.in") as lines:
    for line in lines:
        data.append(list(map(int, line.split())))


def extrapolate(row: list[list[int]]):
    newrows: list[list[int]] = [row.copy()]
    while True:
        newrow = []
        for v1, v2 in zip(row[:-1], row[1:]):
            newrow.append(v2 - v1)

        # print(row, "-->", newrow)

        newrows.append(newrow)
        if all(v == 0 for v in newrow):
            break

        row = newrow

    newrows[-1].append(0)  # all zeroes
    currval: int = 0
    for oldrow in newrows[-2::-1]:
        currval = oldrow[-1] + currval
        oldrow.append(currval)

    return currval


def extrapolate_before(row: list[int]):
    newrows: list[list[int]] = [row.copy()]
    while True:
        newrow = []
        for v1, v2 in zip(row[:-1], row[1:]):
            newrow.append(v2 - v1)

        print(row, "-->", newrow)

        newrows.append(newrow)
        if all(v == 0 for v in newrow):
            break

        row = newrow

    history: list[list[int]] = []
    currval: int = 0
    for r in newrows[::-1]:
        currval = r[0] - currval
        history.append([currval] + r)

    for row in history:
        print(row)

    return currval


part1 = 0
for row in data:
    newval = extrapolate(row.copy())
    part1 += newval

print(part1)

part2 = 0
for row in data:
    newval = extrapolate_before(row.copy())
    print(newval)
    print()
    part2 += newval

print(part2)
