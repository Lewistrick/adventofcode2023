from tqdm import tqdm
from helpers import DIRS4, Pos


def show_grid(hs, gridsizex, gridsizey, o, a):
    minx = min(x for x, y in o)
    miny = min(y for x, y in o)
    maxx = max(x for x, y in o) + 1
    maxy = max(y for x, y in o) + 1

    for y in range(miny - 5, maxy + 5):
        for x in range(minx - 5, maxx + 5):
            if (x % gridsizex, y % gridsizey) in hs:
                print("#", end="")
            elif (x, y) in o:
                print("O", end="")
            elif (x, y) in a:
                print(".", end="")
            else:
                print(" ", end="")
        print()


def solve(hs: set[Pos], maxx: int, maxy: int, start: Pos, nsteps, part1=True) -> int:
    outer_ring: set[Pos] = set()
    outer_ring.add(start)
    prev_outer_ring: set[Pos] = set()
    n_seen_even = 1  # start
    n_seen_uneven = 0
    for step in tqdm(range(nsteps)):
        next_outer_ring: set[Pos] = set()
        for x, y in outer_ring:
            for dx, dy in DIRS4:
                newx, newy = (x + dx, y + dy)
                if (newx, newy) in prev_outer_ring:
                    continue
                if part1:
                    if newx < 0 or newy < 0 or newx >= maxx or newy >= maxy:
                        continue
                    if (newx, newy) in hs:
                        continue
                else:
                    if (newx % (maxx + 1), newy % (maxy + 1)) in hs:
                        continue

                next_outer_ring.add((newx, newy))

        prev_outer_ring = outer_ring.copy()
        outer_ring = next_outer_ring.copy()

        # we start at step 0, which is even; puzzle counts this as step 1
        if step % 2 == 1:
            n_seen_even += len(outer_ring)
        else:
            n_seen_uneven += len(outer_ring)

        # show_grid(hs, maxx + 1, maxy + 1, outer_ring, all_seen)
        # print(f"After {step+1} steps: {n_seen_even=} {n_seen_uneven=}")
        # input(">>")

    if nsteps % 2 == 0:
        return n_seen_even
    return n_seen_uneven


start: Pos
with open("21.in") as f:
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
