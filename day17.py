import random
from collections import deque
from typing import Deque

from helpers import DIRS4, DirectionTuple, Pos

Route = Deque[DirectionTuple]
Option = tuple[int, Route]


def show_dists(grid, paths):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            options = paths.get((x, y))
            if not options:
                print("???", end=" ")
                continue
            dist, rt = min(options, key=lambda option: option[0])
            print(f"{dist:3d}", end=" ")
        print()


def solve(
    grid: list[list[int]],
    xsrc: int,
    ysrc: int,
    xtgt: int,
    ytgt: int,
    maxlen: int,
):
    loss = grid[ysrc][xsrc]
    if xsrc == xtgt and ysrc == ytgt:
        return loss

    # Find shortest paths for every point in the grid, where for every (x, y)
    # a list of options to that path is saved; an option is a tuple of:
    # - the loss to that point given that option
    # - the last 3 steps taken to that point given that option
    # (only options less than 30 above the minimum are saved)
    shortest_paths: dict[Pos, list[Option]] = {
        (xsrc, ysrc): [(0, deque(maxlen=maxlen))]
    }
    queue: list[Pos] = [(xsrc, ysrc)]
    while queue:
        (x_, y_) = queue.pop(0)
        for currloss, curr_route in shortest_paths[(x_, y_)]:
            for dx, dy in DIRS4:
                newx, newy = x_ + dx, y_ + dy
                if newx < 0 or newx >= len(grid[0]) or newy < 0 or newy >= len(grid):
                    # can't go outside grid
                    continue
                if curr_route and curr_route[-1] == (-dx, -dy):
                    # can't go backwards
                    continue
                if len(curr_route) == maxlen and all(d == (dx, dy) for d in curr_route):
                    # can't go more than `maxlen` times in the same direction
                    continue

                # If a minimal loss to the new point already was calculated,
                # add this new path as an option if it's within 30 loss of the existing
                newroute = curr_route.copy()
                newroute.append((dx, dy))

                newloss = currloss + grid[newy][newx]
                options = shortest_paths.get((newx, newy), [])
                if any(
                    oloss <= newloss and oroute == newroute for oloss, oroute in options
                ):
                    # This option was already checked
                    continue

                if options:
                    prevloss, _ = min(options, key=lambda option: option[0])
                    if newloss > prevloss + 30:
                        continue
                    # print(f"Options to {(newx, newy)}:")
                    # for option in sorted(options):
                    # print("-", option)
                    # if len(options) > 1:
                    #     breakpoint()

                # A new route with minimal loss was found to (newx, newy)!
                new_option = (newloss, newroute)
                # print(f"New option to {(newy, newx)}: {new_option}")

                # Save the option to the new point
                if options:
                    shortest_paths[(newx, newy)].append(new_option)
                else:
                    shortest_paths[(newx, newy)] = [new_option]

                # Update the queue (we need to update neighbors of this point too!)
                queue.append((newx, newy))
        if random.random() < 0.001:
            show_dists(grid, shortest_paths)

    options = shortest_paths[(xtgt, ytgt)]
    # for solution, route in sorted(options, key=lambda option: option[0]):
    #     print(route)

    solution, route = min(options)

    return solution


with open("17.ex") as f:
    lines = f.read().split("\n")
    grid = [[int(i) for i in row] for row in lines]

x, y = 0, 0
maxx, maxy = len(grid[0]) - 1, len(grid) - 1
part1 = solve(grid, x, y, maxx, maxy, 3)
print(part1)
