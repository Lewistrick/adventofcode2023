from helpers import DIRS4, Pos


def show_grid(hs, gridsizex, gridsizey, o):
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
            else:
                print(" ", end="")
        print()


def solve(hs: set[Pos], maxx: int, maxy: int, start: Pos, nsteps, part2=False) -> int:
    reached: set[Pos] = set()
    reached.add(start)
    for step in range(nsteps):
        new_reached: set[Pos] = set()
        for x0, y0 in reached:
            for dx, dy in DIRS4:
                newx, newy = x0 + dx, y0 + dy
                if not part2:
                    if newx < 0 or newy < 0 or newx >= maxx or newy >= maxy:
                        continue
                    if (newx, newy) in hs:
                        continue
                else:
                    if (newx % (maxx + 1), newy % (maxy + 1)) in hs:
                        continue

                new_reached.add((newx, newy))
        reached = new_reached

    # show_grid(hs, maxx + 1, maxy + 1, reached)
    # print(f"After {step+1} steps: {len(reached)} seen")
    # input(">>")
    return len(reached)


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

for nsteps in (6, 7, 10, 50, 100, 500, 1000, 5000):
    test = solve(garden_plots, maxx, maxy, start, nsteps, part2=True)
    print(nsteps, test)

# part2 = solve(garden_plots, maxx, maxy, start, 26501365, True)
