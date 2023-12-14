with open("14.in") as h:
    lines = h.read().split("\n")

# Just save the coordinates of every type
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


SORTERS = {
    "north": lambda r: r[1],
    "south": lambda r: -r[1],
    "east": lambda r: -r[0],
    "west": lambda r: r[0],
}

DIRECTIONS = {
    "north": (0, -1),
    "south": (0, 1),
    "east": (1, 0),
    "west": (-1, 0),
}


def on_limit(x, y, direction, maxx, maxy):
    """Check if (x, y) is on the edge of the grid with size (maxx+1, maxy+1).

    Only returns True if (x, y) is on the edge defined by {direction}.
    """
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
    """Roll all stones as far as possible in a given direction."""
    # The sorter is used to move stones in the right order; stones closest to the
    # given direction will be moved first.
    sorter = SORTERS[direction]
    dx, dy = DIRECTIONS[direction]
    while True:
        # Every iteration in this loop moves all stones that can move
        # one tile in the given direction.
        # It keeps track of the number of moves per iteration.
        n_moves = 0
        new_stones = set()
        for x, y in sorted(stones, key=sorter):
            # A stone can't move when:
            # - it's already on the edge in the given direction
            # - there's a cube in the way
            # - there's an (possibly already moved) round stone in the way
            p = (x + dx, y + dy)
            if on_limit(x, y, direction, maxx, maxy) or p in cubes or p in new_stones:
                new_stones.add((x, y))
                continue

            # Move the stone
            n_moves += 1
            new_stones.add(p)
            empties.remove(p)
            empties.add((x, y))

        # Replace the old stones in the grid by the new stones
        stones = new_stones

        # If no stones moved in this iteration, we're done moving.
        if n_moves == 0:
            break

    return stones, empties


def show_grid(lines, rounds, empties, with_line_nos=False):
    """Show the grid.

    Args:
        lines: the base grid
        rounds: the round stones at the current move
        empties: the empty cells at the current move
        with_line_nos: if true, print line numbers at the right of the grid
            (these are used for calculating score)
    """
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


def calc_total_load(rounds, maxy):
    return sum(maxy - y + 1 for _, y in rounds)


def spin(rounds, empties, spin_order, maxx, maxy):
    """Spin the grid in the given order.

    Grid is defined by rounds, empties and cubes (the latter is static).
    The spin_order should consist of any number of wind directions.
    """
    for sd in spin_order:
        rounds, empties = roll(rounds.copy(), empties.copy(), sd, maxx, maxy)
    return rounds, empties


maxx = len(lines[0]) - 1
maxy = len(lines) - 1

rounds_p1, empties_p1 = roll(rounds.copy(), empty.copy(), "north", maxx, maxy)


part1 = calc_total_load(rounds_p1, maxy)
print(part1)

rounds_p2 = rounds.copy()
empties_p2 = empty.copy()
spin_order = ("north", "west", "south", "east")


hashes = {}  # {spin_hash : spin_cycle}
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
