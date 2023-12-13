def clean_input(input_: str) -> list[list[str]]:
    grid = []
    for row in input_.split("\n"):
        if not row.strip():
            continue
        grid.append(list(row.strip()))
    return grid


def solve(rows):
    lastrow = ""
    for i, row in enumerate(rows):
        if lastrow != row:
            lastrow = row
            continue

        mirror = True
        for i1, i2 in zip(range(i - 1, -1, -1), range(i, len(rows))):
            row1, row2 = rows[i1], rows[i2]
            print("Comparing:")
            print(f"{i1+1:2d}", " ".join(row1))
            print(f"{i2+1:2d}", " ".join(row2), end=" ")
            print("equal" if row1 == row2 else "different")
            if row1 != row2:
                mirror = False
                break
        else:
            return i

        lastrow = row
    return 0


def show_grid(grid):
    for row in grid:
        print(" ".join(row))


with open("13.in") as file:
    inputs = file.read().split("\n\n")

grids = [clean_input(input_) for input_ in inputs]

for grid in grids:
    show_grid(grid)
    print(solve(grid))
    break
    # solve(rotate(grid))
