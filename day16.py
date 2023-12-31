from collections import defaultdict
from functools import reduce

from helpers import Pos, ddir

with open("16.in") as f:
    lines = f.read().split()

mirrors = {}
empty = set()
for y, line in enumerate(lines):
    for x, ch in enumerate(line.strip()):
        if ch == ".":
            empty.add((x, y))
            continue
        mirrors[(x, y)] = ch


def solve_by_start(
    mirrors: dict[Pos, str],
    empty: set[Pos],
    start: Pos,
    startd: str,
):
    q = [(start, startd)]
    seen: dict[str, set[tuple[int, int]]] = defaultdict(set)
    while q:
        (x, y), d = q.pop()

        # Outside maze
        if (x, y) not in empty and (x, y) not in mirrors:
            continue

        # Mark as seen in this direction
        seen[d].add((x, y))

        if (x, y) in empty:
            dx, dy = ddir[d]
            newx, newy = x + dx, y + dy

            if (newx, newy) in seen[d]:
                continue

            q.append(((newx, newy), d))
            continue

        match mirrors[(x, y)], d:
            case "|", "L" | "R":
                for nd in "UD":
                    dx, dy = ddir[nd]
                    q.append(((x + dx, y + dy), nd))
                continue
            case "|", "U" | "D":
                dx, dy = ddir[d]
                nd = d
            case "-", "L" | "R":
                dx, dy = ddir[d]
                nd = d
            case "-", "U" | "D":
                for nd in "LR":
                    dx, dy = ddir[nd]
                    q.append(((x + dx, y + dy), nd))
                continue
            case "/", "R":
                nd = "U"
            case "/", "L":
                nd = "D"
            case "/", "U":
                nd = "R"
            case "/", "D":
                nd = "L"
            case "\\", "R":
                nd = "D"
            case "\\", "L":
                nd = "U"
            case "\\", "U":
                nd = "L"
            case "\\", "D":
                nd = "R"
            case m, d:
                raise ValueError(f"Wrong m/d: {m} {d}")

        dx, dy = ddir[nd]
        q.append(((x + dx, y + dy), nd))

    return len(reduce(lambda s1, s2: s1 | s2, seen.values()))


maxx = max(x for (x, y) in empty)
maxy = max(y for (x, y) in empty)

part1 = solve_by_start(mirrors, empty, (0, 0), "R")
print(part1)

part2 = 0
for x in range(maxx):
    part2 = max(part2, solve_by_start(mirrors, empty, (x, 0), "D"))
    part2 = max(part2, solve_by_start(mirrors, empty, (x, maxy), "U"))

for y in range(maxy):
    part2 = max(part2, solve_by_start(mirrors, empty, (0, y), "R"))
    part2 = max(part2, solve_by_start(mirrors, empty, (maxx, y), "L"))

print(part2)
