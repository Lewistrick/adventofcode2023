import sys
from collections import defaultdict
from typing import Optional

from matplotlib import pyplot as plt
from tqdm import tqdm

example = "-e" in sys.argv

Pos = tuple[int, int]
nodes: dict[Pos, list[Pos]] = defaultdict(list)  # (x_from, y_from): [(x_to, y_to), ...]
spaces: set[Pos] = set()

start: Optional[Pos] = None
file = "10.example.in" if example else "10.in"
with open(file) as lines:
    for y, line in enumerate(lines, 1):
        for x, ch in enumerate(line.strip(), 1):
            match ch:
                case ".":
                    spaces.add((x, y))
                case "|":
                    nodes[(x, y)].append((x, y - 1))
                    nodes[(x, y)].append((x, y + 1))
                case "-":
                    nodes[(x, y)].append((x - 1, y))
                    nodes[(x, y)].append((x + 1, y))
                case "L":
                    nodes[(x, y)].append((x, y - 1))
                    nodes[(x, y)].append((x + 1, y))
                case "J":
                    nodes[(x, y)].append((x, y - 1))
                    nodes[(x, y)].append((x - 1, y))
                case "7":
                    nodes[(x, y)].append((x - 1, y))
                    nodes[(x, y)].append((x, y + 1))
                case "F":
                    nodes[(x, y)].append((x + 1, y))
                    nodes[(x, y)].append((x, y + 1))
                case "S":
                    start = (x, y)
                case _:
                    raise ValueError("Unknown node type")

prev1 = tuple(start)
prev2 = tuple(start)
# start position directions are south and west (done visually)
curr1 = (start[0] - 1, start[1])  # west
if example:
    curr1 = (start[0] + 1, start[1])  # east
curr2 = (start[0], start[1] + 1)  # south
nodes[start] = [curr1, curr2]
part1 = 1


def do_step(prev: Pos, curr: Pos):
    poss1, poss2 = nodes[curr]
    newcurr = poss2 if poss1 == prev else poss1
    newprev = curr
    return newprev, newcurr


loop: set[Pos] = {start}
connections: set[tuple[Pos, Pos]] = set()
while curr1 != curr2:
    loop.add(curr1)
    loop.add(curr2)
    connections.add(tuple(sorted((prev1, curr1))))
    connections.add(tuple(sorted((prev2, curr2))))
    prev1, curr1 = do_step(prev1, curr1)
    prev2, curr2 = do_step(prev2, curr2)

    part1 += 1

loop.add(curr1)
connections.add((prev1, curr1))
connections.add((prev2, curr2))

print(part1)
print(len(loop))

junkpipes = {node for node in nodes if node not in loop}
spaces |= junkpipes
print(len(spaces), "spaces total")

# pick one node that is outside the loop
base_outside: Pos = (1, 3)


# for every node in `spaces`, create a line from there to base_outside;
# if it intersects an odd number of node connections, it is inside the loop
# if it intersects an even number of node connections, it is outside the loop
def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])


def intersects(a, b, c, d):
    """Return True if line segments ab and cd intersect"""
    return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)


inside: set[Pos] = set()
outside: set[Pos] = set()
for node in tqdm(spaces):
    if node in inside or node in outside:
        continue
    intersections: list[tuple[Pos, Pos]] = []
    non_intersections: list[tuple[Pos, Pos]] = []
    for conn in connections:
        if intersects(node, base_outside, *conn):
            intersections.append(conn)
        else:
            non_intersections.append(conn)
    if node == (20, 1):
        print()
        for line in sorted(intersections):
            plt.plot(*list(zip(*line)), color="green")
        for line in sorted(non_intersections):
            plt.plot(*list(zip(*line)), color="red")
        plt.plot(*list(zip(node, base_outside)), color="black")
        plt.show()
        breakpoint()
    if len(intersections) % 2 == 0:
        outside.add(node)
    else:
        inside.add(node)

    # optimization: for every node connecting to this node,
    # find direct neighbors (these are in the same group as this node)

print(len(inside), "inside")  # part2; 299 is too high
print(len(outside), "outside")

maxx = max(x for x, y in nodes)
maxy = max(y for x, y in nodes)

for y in range(1, maxy + 1):
    for x in range(1, maxx + 1):
        node = (x, y)
        if node in inside:
            print("I", end="")
        elif node in outside:
            print("O", end="")
        elif node in loop:
            print(" ", end="")
        else:
            print("?", end="")
    print()
