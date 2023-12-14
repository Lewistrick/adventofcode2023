with open("14.in") as h:
    lines = h.read().split("\n")

empty = set()
rounds = set()
cubes = set()
for y, line in enumerate(lines):
    for x, cell in enumerate(line):
        if cell == ".":
            empty.add((x, y))
        elif cell == "O":
            rounds.add((x, y))
        elif cell == "#":
            cubes.add((x, y))


sorters = {
    "north": lambda r: r[1],
    "south": lambda r: -r[1],
    "east": lambda r: -r[0],
    "west": lambda r: r[0],
}

directions = {
    "north": (0, -1),
    "south": (0, 1),
    "east": (1, 0),
    "west": (-1, 0),
}

maxx = len(lines[0]) - 1
maxy = len(lines) - 1


def on_limit(x, y, direction, maxx, maxy):
    if direction == "north" and y == 0:
        return True
    if direction == "south" and y == maxy:
        return True
    if direction == "east" and x == maxx:
        return True
    if direction == "west" and x == 0:
        return True
    return False


def roll(
    stones: set[tuple[int, int]],
    empties: set[tuple[int, int]],
    direction: str,
    maxx: int,
    maxy: int,
):
    sorter = sorters[direction]
    dx, dy = directions[direction]
    while True:
        n_moves = 0
        new_stones = set()
        for x, y in sorted(stones, key=sorter):
            p = (x + dx, y + dy)
            if on_limit(x, y, direction, maxx, maxy) or p in cubes or p in new_stones:
                new_stones.add((x, y))
                continue

            # print(f"Moving {(x,y)} {direction} to {p}")

            n_moves += 1
            new_stones.add(p)
            empties.remove(p)
            empties.add((x, y))

        stones = new_stones
        if n_moves == 0:
            break
    return stones, empties


def show_grid(lines, rounds, empties, with_line_nos=False):
    for y, line in enumerate(lines):
        for x, cell in enumerate(line):
            if (x, y) in rounds:
                ch = "O"
            elif (x, y) in empties:
                ch = "."
            else:
                ch = cell
            print(ch, end="")
        if with_line_nos:
            print("", maxy - y + 1)
        else:
            print()


rounds_p1, empties_p1 = roll(rounds.copy(), empty.copy(), "north", maxx, maxy)


def calc_total_load(rounds, maxy):
    score = 0
    for x, y in rounds:
        score += maxy - y + 1

    return score


part1 = calc_total_load(rounds_p1, maxy)
print(part1)

rounds_p2 = rounds.copy()
empties_p2 = empty.copy()
spin_order = ("north", "west", "south", "east")


def spin(rounds, empties, spin_order, maxx, maxy):
    for sd in spin_order:
        rounds, empties = roll(rounds.copy(), empties.copy(), sd, maxx, maxy)
    return rounds, empties


hashes = {}  # spin_hash : spin_cycle
load_sizes = []
cycle_size = 0
cycle_start = 0
for spin_cycle in range(1000000000):
    rounds_p2, empties_p2 = spin(
        rounds_p2.copy(), empties_p2.copy(), spin_order, maxx, maxy
    )
    spin_hash = hash(tuple(sorted(rounds_p2) + sorted(empties_p2)))
    if spin_hash in hashes:
        old_cycle = hashes[spin_hash]
        cycle_size = spin_cycle - old_cycle
        cycle_start = old_cycle
        break
    hashes[spin_hash] = spin_cycle
    load_sizes.append(calc_total_load(rounds_p2, maxy))


remainder = (1000000000 - cycle_start) % cycle_size
target_cycle = cycle_start + remainder - 1
print(load_sizes[target_cycle])
