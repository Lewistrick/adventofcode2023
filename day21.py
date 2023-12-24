from collections import defaultdict
from tqdm import tqdm
from helpers import DIRS4, Pos
from typing import DefaultDict


def show_grid(hs, gridsizex, gridsizey, curr, nvisited):
    for y in range(gridsizey + 1):
        for x in range(gridsizex + 1):
            if (x % gridsizex, y % gridsizey) in hs:
                value = "#"
            elif (x, y) in curr:
                value = f"*{nvisited[(x,y)]}"
            elif (x, y) in nvisited:
                value = f" {nvisited[(x, y)]}"
            else:
                value = ""

            print(f"{value:>5}", end="")
        print()


def solve(hs: set[Pos], maxx: int, maxy: int, start: Pos, nsteps, part1=True) -> int:
    """The new plan: work with projected starts.

    1. Get the minimum distance to a projected start field in each direction (also diag)
        For the example input, the minimum distance in all directions are as follows:

        26  21  22
        15   0  15
        22  21  26

        This is, of course, mirrored: when travelling north, the same blocks are
        used as when travelling south, just in different plots of land. The same goes
        for the combinations E/W, NW/SE and NE/SW.

    2. Calculate the number of projected starts that can be reached within the given
        amount of steps.
    """

    # save the positions reached
    current_positions: set[Pos] = set()
    current_positions.add(start)
    # save number of times visited for each cell
    n_visited: DefaultDict[Pos, int] = defaultdict(int)
    n_visited[start] = 1

    print(f"Added {len(new_positions)} positions after step {step}")
    current_positions = new_positions
    for pos in current_positions:
        n_visited[pos] += 1

    show_grid(hs, maxx + 1, maxy + 1, current_positions, n_visited)

    return sum(n_visited[cell] for cell in current_positions)


start: Pos
with open("21.ex") as f:
    garden_plots = set()
    maxx, maxy = 0, 0
    for y, row in enumerate(f):
        for x, col in enumerate(row.strip()):
            if col == "#":
                garden_plots.add((x, y))
            elif col == "S":
                start = (x, y)
            maxx = x
        maxy = y

part1 = solve(garden_plots, maxx, maxy, start, 64)
print(part1)
assert part1 == 3699

# nsteps_test = (6, 10, 50, 100, 500, 1000, 5000)
# test_solutions = (16, 50, 1594, 6536, 167004, 668697, 16733044)
# for nsteps, solution in zip(nsteps_test, test_solutions):
#     test = solve(garden_plots, maxx, maxy, start, nsteps, part1=False)
#     print(nsteps, test, "=?", solution)
#     assert test == solution

part2 = solve(garden_plots, maxx, maxy, start, 26501365, False)
print(part2)
