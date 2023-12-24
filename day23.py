from heapq import heappop, heappush
from helpers import DIRS4, DirectionTuple, Pos, ddir
from typing import TypeAlias

# currpos, prevpos, distance
QueueElement: TypeAlias = tuple[Pos, Pos, int]
# heap_prio, currpos, visited, distance
QueueElement2: TypeAlias = tuple[int, Pos, set[Pos], int]


def show(paths, minx, maxx, miny, maxy, slopes, currpos, prevpos, visited):
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            if (x, y) == currpos:
                value = "*"
            elif (x, y) == prevpos:
                value = "-"
            elif (x, y) in slopes:
                value = "?"
            elif (x, y) in visited:
                value = "."
            elif (x, y) in paths:
                value = " "
            else:
                value = "#"
            print(value, end="")
        print()
    input(">>")


paths: set[Pos] = set()
slopes: dict[Pos, DirectionTuple] = {}
start: Pos = None
minx, miny = 0, 0
with open("23.ex") as f:
    for y, line in enumerate(f):
        for x, ch in enumerate(line.strip()):
            if ch == ".":
                if start is None:
                    start = (x, y)
                paths.add((x, y))
                finish = (x, y)
            elif ch == "#":
                continue
            else:
                slopes[(x, y)] = ddir[ch]

    maxx, maxy = x, y


def p1(paths: set[Pos], slopes: dict[Pos, DirectionTuple], start: Pos, finish: Pos):
    queue: list[QueueElement] = [(start, (-1, -1), 1)]
    solutions = []
    visited = set()
    while queue:
        ((currx, curry), (prevx, prevy), dist) = queue.pop()

        visited.add((currx, curry))
        # show(paths, minx, maxx, miny, maxy, slopes, (currx, curry), (prevx, prevy), visited)

        for dx, dy in DIRS4:
            newx, newy = currx + dx, curry + dy
            if newx == prevx and newy == prevy:
                continue

            if (newx, newy) in paths:
                queue.append(((newx, newy), (currx, curry), dist + 1))

            if (newx, newy) in slopes:
                if (dx, dy) == slopes[(newx, newy)]:
                    queue.append(((newx, newy), (currx, curry), dist + 1))

            if (newx, newy) == finish:
                solutions.append(dist)

    return max(solutions)


def p2(paths: set[Pos], start: Pos, finish: Pos):
    queue: list[QueueElement2] = [(0, start, {start}, 1)]
    best_solution = 0
    while queue:
        (prio, (currx, curry), visited, dist) = heappop(queue)

        dead_end = True
        for dx, dy in DIRS4:
            newx, newy = currx + dx, curry + dy
            if (newx, newy) == finish:
                if dist > best_solution:
                    print(f"Found solution of length {dist} ({len(queue)=})")
                    best_solution = dist
                else:
                    print(f"Too short: {dist}")
                continue

            if (newx, newy) in visited:
                continue

            if (newx, newy) in paths:
                dead_end = False
                prio = len(paths) - dist
                heappush(
                    queue,
                    (prio, (newx, newy), visited | {(newx, newy)}, dist + 1),
                )

        # if dead_end:
        #     print(f"\rFound dead end of length {dist}", end=" ")
        #     show(paths, minx, maxx, miny, maxy, set(), None, None, visited)

    return best_solution


part1 = p1(paths, slopes, start, finish)
print(part1)

part2 = p2(paths | set(slopes.keys()), start, finish)
print(part2)  # 6398 too low
