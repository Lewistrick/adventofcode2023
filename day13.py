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
        if (total_smudges := calculate_smudges(lastrow, row, i - 1, i)) > 1:
            lastrow = row
            continue

        # print()
        # print("Possible match found...")

        for i1, i2 in zip(range(i - 2, -1, -1), range(i + 1, len(rows))):
            row1, row2 = rows[i1], rows[i2]
            n_smudges = calculate_smudges(row1, row2, i1, i2)
            total_smudges += n_smudges

            if total_smudges > 1:
                # print("Not a match!")
                break

        if total_smudges == 1:
            # print(f"Found match {i=}!")
            return i

        # print(f"{i=} {total_smudges=}")

        lastrow = row

    # print("Checked everything, not a match!")
    return 0


def calculate_smudges(row1, row2, i1, i2):
    n_smudges = sum(1 for e1, e2 in zip(row1, row2) if e1 != e2)
    # print(f"{i1+1:2d}", " ".join(row1))
    # print(f"{i2+1:2d}", " ".join(row2), end=" ")
    # print(f"Found {n_smudges} smudges")
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


with open("13.in") as file:
    inputs = file.read().split("\n\n")

grids = [clean_input(input_) for input_ in inputs]

part1 = 0
part2 = 0
for grid in grids:
    dirg = rotate_clockwise(grid)
    horizontal = solve_p1(grid)
    vertical = solve_p1(dirg)
    part1 += 100 * horizontal + vertical

    # print("-" * 80)

    # show_grid(grid)
    # print()
    hor2 = solve_p2(grid)

    # print("-" * 80)

    # show_grid(dirg)
    # print()
    ver2 = solve_p2(dirg)
    # print("-" * 80)
    # print(hor2, ver2)
    part2 += 100 * hor2 + ver2

print(part1)
print(part2)
