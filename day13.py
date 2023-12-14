def clean_input(input_: str) -> list[list[str]]:
    """Given a grid as lines, make a matrix of it"""
    grid = []
    for row in input_.split("\n"):
        if not row.strip():
            continue
        grid.append(list(row.strip()))
    return grid


def solve_p1(rows: list[str]):
    """Find exact mirrors in the horizontal position.

    To find mirrors in the vertical position, rotate the grid (`rotate_clockwise`).
    """
    lastrow = ""
    for i, row in enumerate(rows):
        # Start checking from the second row onward
        if lastrow != row:
            lastrow = row
            continue

        mirror = True
        # Somehow this doesn't work with indexing the rows. Let's keep the indices.
        for i1, i2 in zip(range(i - 2, -1, -1), range(i + 1, len(rows))):
            row1, row2 = rows[i1], rows[i2]
            if row1 != row2:
                mirror = False
                break

        if mirror:
            return i

        lastrow = row
    return 0


def solve_p2(rows):
    """Find mirrors with smudges (same as p1: in horizontal position)."""
    lastrow = ""
    for i, row in enumerate(rows):
        if lastrow == "":
            lastrow = row
            continue

        # Start from either 0 or 1 smudges.
        if (total_smudges := calculate_smudges(lastrow, row)) > 1:
            lastrow = row
            continue

        # Possible match found! Count the number of smudges; the total should be 1.
        for i1, i2 in zip(range(i - 2, -1, -1), range(i + 1, len(rows))):
            row1, row2 = rows[i1], rows[i2]
            n_smudges = calculate_smudges(row1, row2)
            total_smudges += n_smudges

            # Stop checking if this (theoretical) mirror has too many smudges
            if total_smudges > 1:
                break

        # This is a mirror!
        if total_smudges == 1:
            return i

        # This is not a mirror, keep checking
        lastrow = row

    # Checked all rows, not a match
    return 0


def calculate_smudges(row1, row2):
    """Given a theoretical mirror in the middle between row1 and row2, count the number
    of smudges by comparing every element seen in the mirror on both rows.

    """
    return sum(1 for e1, e2 in zip(row1, row2) if e1 != e2)


def rotate_clockwise(grid):
    """Rotate the grid clockwise.

    Every column in `grid` becomes a reversed row in the new grid.
    """
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
    # Rotating the grid makes sure we can solve for vertical mirrors as well
    dirg = rotate_clockwise(grid)
    # score = 100 * horizontal + 1 * vertical
    part1 += 100 * solve_p1(grid) + solve_p1(dirg)
    part2 += 100 * solve_p2(grid) + solve_p2(dirg)

print(part1)
print(part2)
