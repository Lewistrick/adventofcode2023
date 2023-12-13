import functools

springs = []
with open("12.in") as lines:
    for line in lines:
        spring, countstr = line.strip().split()
        counts = list(map(int, countstr.split(",")))
        springs.append((spring, counts))


@functools.lru_cache(maxsize=1000)
def solve(record: str, counts: tuple[int]) -> int:
    if not counts:
        if all(ch in ".?" for ch in record):
            return 1
        return 0

    n_solutions = 0
    count, rest_counts = counts[0], counts[1:]

    # Find all positions where `count` would fit
    for start in range(len(record) - count + 1):
        if any(ch == "#" for ch in record[:start]):
            break
        end = start + count
        subrecord = record[start:end]

        # Check if this spring fits
        if all(ch in "?#" for ch in subrecord):
            if end < len(record) and record[end] == "#":
                continue
            if start > 0 and record[start - 1] == "#":
                continue

            new_subrecord = record[end + 1 :]
            n_sub_solutions = solve(new_subrecord, rest_counts)
            n_solutions += n_sub_solutions

    return n_solutions


part1 = 0
for spring, counts in springs:
    subp1 = solve(spring, tuple(counts))
    part1 += subp1
print(part1)  # 9001 too high, 7323 too high, 6827 correct

part2 = 0
for spring, counts in springs:
    new_spring = "?".join(spring for _ in range(5))
    new_counts = tuple(counts * 5)
    subp2 = solve(new_spring, new_counts)
    part2 += subp2
print(part2)
