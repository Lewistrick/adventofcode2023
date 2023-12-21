from itertools import count

with open("21.ex") as f:
    garden_plots = set()
    start = (0, 0)
    for y, row in enumerate(f):
        for x, col in enumerate(row.strip()):
            if col == "#":
                garden_plots.add((x, y))
            elif col == "S":
                start = (x, y)


def solve(x: int, y: int, nsteps) -> int:
    reached = set((x, y))
    for step in range(nsteps):
        new_reached = set()
        for dx, dy in DIRS4:
            ...


part1 = solve(*start, 64)
