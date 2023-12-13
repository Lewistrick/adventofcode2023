grid = []
galaxies = []
with open("11.in") as lines:
    for y, line in enumerate(lines):
        grid.append(list(line.strip()))
        xs = (i for i, ch in enumerate(line.strip()) if ch == "#")
        galaxies += [(x, y) for x in xs]

empty_row_ids = {i for i, row in enumerate(grid) if all(ch == "." for ch in row)}
empty_col_ids = {i for i in range(len(grid)) if all(row[i] == "." for row in grid)}


part1 = 0
part2 = 0
for g1, (x1, y1) in enumerate(galaxies[:-1], 1):
    for g2, (x2, y2) in enumerate(galaxies[g1:], g1 + 1):
        xrange = range(min(x1, x2), max(x1, x2))
        yrange = range(min(y1, y2), max(y1, y2))

        x_travels = sum(1 for row in empty_col_ids if row in xrange)
        y_travels = sum(1 for col in empty_row_ids if col in yrange)

        dist = x_travels + y_travels + abs(x1 - x2) + abs(y1 - y2)
        dist2 = 999_999 * x_travels + 999_999 * y_travels + abs(x1 - x2) + abs(y1 - y2)

        part1 += dist
        part2 += dist2

print(part1)
print(part2)
