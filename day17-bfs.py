from typing import Generator

from helpers import DIRS4, Pos


def diffs(route: list[Pos], n) -> Generator[Pos, None, None]:
    for (x1, y1), (x2, y2) in zip(route[: -n - 1 : -1], route[-2 : -n - 2 : -1]):
        dx, dy = x1 - x2, y1 - y2
        yield (dx, dy)


def solve(
    grid: list[list[int]],
    xsrc: int,
    ysrc: int,
    xtgt: int,
    ytgt: int,
    maxlen: int,
    seen: list[Pos] | None = None,
):
    # The shortest route to r(x,y) is min(r(x',y') : (x',y')<->(x,y)) + v(x,y)
    # in which <-> means 'borders'
    # and v(x,y) is the value at (x,y) in the grid.
    # print(xtgt, ytgt, seen)

    # Base case: we're at src.
    if xsrc == xtgt and ysrc == ytgt:
        return grid[ysrc][xsrc]

    if seen is None:
        print("Setting seen")
        seen = []

    # print("\r" + "#" * len(seen), end="                ")

    solutions: list[Pos] = []
    for dx, dy in DIRS4:
        newx, newy = xtgt + dx, ytgt + dy
        if newx < 0 or newy < 0 or newx >= len(grid[0]) or newy >= len(grid):
            # can't go outside of grid
            continue

        if (newx, newy) in seen:
            # can't revisit cells
            continue

        if len(seen) > 3 and all(diff == (dx, dy) for diff in diffs(seen, 3)):
            # if the last 3 directions (dx, dy) were equal,
            # don't have this one be equal too
            continue

        solution = solve(grid, xsrc, ysrc, newx, newy, maxlen, seen + [(newx, newy)])
        if solution is not None:
            solution += grid[xsrc][ysrc]
            solutions.append(solution)

    if not solutions:
        return None

    return min(solutions)


with open("17.ex2") as f:
    lines = f.read().split("\n")
    grid = [[int(i) for i in row] for row in lines]

x, y = 0, 0
maxx, maxy = len(grid[0]) - 1, len(grid) - 1
part1 = solve(grid, x, y, maxx, maxy, 3)
print(part1)
