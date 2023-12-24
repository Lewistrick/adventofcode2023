from collections import defaultdict
from functools import lru_cache
from helpers import DIRS4, DirectionTuple, Pos, ddir
from typing import TypeAlias
import sys

sys.setrecursionlimit(100_000)

# currpos, prevpos, distance
QueueElement: TypeAlias = tuple[Pos, Pos, int]
# heap_prio, currpos, visited, distance
QueueElement2: TypeAlias = tuple[int, Pos, set[Pos], int]

Route = tuple[Pos]
Option = tuple[Route, int]  # (route, distance)


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


def get_distances(node: Pos, nodes: set[Pos], paths: set[Pos]):
    """Calculate distances to all reachable nodes"""
    queue = [(node, {node})]  # currpos, visited
    distances = {}  # (node1, node2): distance
    while queue:
        (x, y), visited = queue.pop()
        for dx, dy in DIRS4:
            newx, newy = x + dx, y + dy
            if (newx, newy) in visited or (newx, newy) not in paths:
                continue
            if (newx, newy) in nodes:
                distances[(newx, newy)] = len(visited)
                # print(node, (newx, newy), "-->", len(visited))
                # show(paths, minx, maxx, miny, maxy, set(), node, (newx, newy), visited)
            else:
                queue.append(
                    (
                        (newx, newy),
                        visited | {(newx, newy)},
                    )
                )
    # for (n1, n2), d in distances.items():
    #     print(n1, "->", n2, ":", d)
    # input(">>")
    return distances


def get_longest_distance(S: Pos, F: Pos, dists: dict[Pos, dict[Pos, int]]):
    """Get the longest distance from node S (start) to node F (finish)
    given direct distances between nodes.
    """
    route1, dist1 = (S,), 0
    options: dict[Pos, list[Option]] = defaultdict(list)  # {node: [Option]}
    options[S].append((route1, dist1))

    queue = [(S, 0)]  # (node, option_id)
    while queue:
        node, routeid = queue.pop(0)
        route, dist = options[node][routeid]
        for newnode, ddist in dists[node].items():
            if newnode in route:
                continue

            newroute: Route = (*route, newnode)
            options[newnode].append((newroute, dist + ddist))
            queue.append((newnode, len(options[newnode]) - 1))

    return max(dist for route, dist in options[F])


def p2(paths: set[Pos], start: Pos, finish: Pos):
    """New plan:

    - determine crossroads (x,y) (aka Nodes)
    - make a network of nodes
    - connect crossroads that can be connected, giving their distance
    - given these nodes, find the longest distance from start to finish
    """
    nodes = {start, finish}
    for x, y in paths:
        n_directions = sum(1 for (dx, dy) in DIRS4 if (x + dx, y + dy) in paths)
        if n_directions > 2:
            nodes.add((x, y))

    distances: dict[Pos, dict[Pos, int]] = {}  # {node: {node: dist}}
    for node in nodes:
        distances[node] = get_distances(node, nodes, paths)

    for n1 in sorted(distances):
        for n2 in sorted(distances[n1]):
            d = distances[n1][n2]
            print(n1, n2, d)

    return get_longest_distance(start, finish, distances)


paths: set[Pos] = set()
slopes: dict[Pos, DirectionTuple] = {}
start: Pos = None
minx, miny = 0, 0
with open("23.in") as f:
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

part2 = p2(paths | set(slopes.keys()), start, finish)
print(part2)  # 6398 too low
