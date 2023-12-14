def clean_input(input_: str) -> list[list[str]]:
    grid = []
    for row in input_.split("\n"):
        if not row.strip():
            continue
        grid.append(list(row.strip()))
    return grid


def solve_p1(rows):
    lastrow = ""
    for i, row in enumerate(rows):
        if lastrow != row:
            lastrow = row
            continue

        mirror = True
        for i1, i2 in zip(range(i - 1, -1, -1), range(i, len(rows))):
            row1, row2 = rows[i1], rows[i2]
            # print("Comparing:")
            # print(f"{i1+1:2d}", " ".join(row1))
            # print(f"{i2+1:2d}", " ".join(row2), end=" ")
            # print("equal" if row1 == row2 else "different")
            if row1 != row2:
                mirror = False
                break

        if mirror:
            return i

        lastrow = row
    return 0


def solve_p2(rows):
    lastrow = ""
    for i, row in enumerate(rows):
        if lastrow == "":
            lastrow = row
            continue

        # Start with 0 or 1 total smudges (more means no mirror)
        if (total_smudges := calculate_smudges(lastrow, row, i - 1, i)) > 1:
            lastrow = row
            continue

        print("Found possible match!")

        for i1, i2 in zip(range(i - 1, -1, -1), range(i, len(rows))):
            row1, row2 = rows[i1], rows[i2]
            n_smudges = calculate_smudges(row1, row2, i1, i2)
            total_smudges += n_smudges

            if total_smudges > 1:
                break

        if total_smudges == 1:
            print("Match found!")
            return i
        else:
            print("Not a match!")

        lastrow = row
    return 0


def calculate_smudges(row1: str, row2: str, i1: int, i2: int):
    print("Comparing:")
    print(f"{i1+1:2d}", " ".join(row1))
    print(f"{i2+1:2d}", " ".join(row2), end=" ")
    n_smudges = sum(1 for e1, e2 in zip(row1, row2) if e1 != e2)
    print(f"Found {n_smudges} smudges")
    return n_smudges


def show_grid(grid):
    for row in grid:
        print(" ".join(str(el) for el in row))


def rotate_clockwise(grid):
    # every column in `grid` becomes a reversed row in the new grid
    dirg = []
    for i in range(len(grid[0])):
        dirg.append([row[i] for row in grid][::-1])
    return dirg


with open("13.ex") as file:
    inputs = file.read().split("\n\n")

grids = [clean_input(input_) for input_ in inputs]

part1 = 0
part2 = 0
for grid in grids:
    dirg = rotate_clockwise(grid)
    horizontal = solve_p1(grid)
    vertical = solve_p1(dirg)
    part1 += 100 * horizontal + vertical

    print("-" * 80)
    show_grid(grid)
    hor2 = solve_p2(grid)
    print(f"Solution: {hor2=}")
    print("-" * 80)
    show_grid(dirg)
    breakpoint()
    ver2 = solve_p2(dirg)
    print(f"Solution: {ver2=}")
    print("-" * 80)
    # print(hor2, ver2)
    # breakpoint()
    part2 += 100 * horizontal + vertical

print(part1)
print(part2)
