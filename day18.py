from typing import Iterable

from helpers import Pos, ddir

Digline = tuple[Pos, Pos]  # (from, to)


def print_trench(trench, inside, minx, maxx, miny, maxy):
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            if (x, y) in trench:
                print("#", end="")
            elif (x, y) in inside:
                print("O", end="")
            else:
                print(".", end="")
        print()


def solve(digs: Iterable[tuple[Pos, int]]):
    currx, curry = 0, 0
    trench: list[Digline] = []

    minx = currx
    maxx = currx
    miny = curry
    maxy = curry

    for (dx, dy), n in digs:
        newx = currx + dx * n
        newy = curry + dy * n
        trench.append(((currx, curry), (newx, newy)))

        currx, curry = newx, newy

        minx = min(currx, minx)
        maxx = max(currx, maxx)
        miny = min(curry, miny)
        maxy = max(curry, maxy)

    assert currx == curry == 0, f"{currx=} {curry=}"

    print(
        minx,
        maxx,
        miny,
        maxy,
    )

    # this is the long part: we need to traverse many rows
    for row in range(miny, maxy + 1):
        # find all ranges for this row
        hranges = {(x1, x2) for ((x1, y1), (x2, y2)) in trench if y1 == y2 == row}
        vranges = {
            x1
            for ((x1, y1), (x2, y2)) in trench
            if x1 == x2 and (y1 < row < y2 or y1 > row > y2)
        }

        # sort the intersections;
        # after every intersection, determine if we are inside or outside the trench
        # (crossing a vrange means that we switch)
        # using the previous (in/out) ranges;
        # then fill that range until we meet another intersection


digs = []

with open("18.ex2") as lines:
    for line in lines:
        if not line.strip():
            break
        d, n, color = line.split()
        digs.append((d, int(n), color[2:-1]))

part1 = solve((ddir[d], n) for (d, n, c) in digs)
print(part1)
# assert part1 == 39039 or part1 == 62

digs2 = []
for d, n, color in digs:
    dir_ = ddir["RDLU"[int(color[-1])]]
    dist = int(color[:-1], 16)
    digs2.append((dir_, dist))

solve(digs2)
