from tqdm import tqdm

springs = []
with open("12.in") as lines:
    for line in lines:
        spring, countstr = line.strip().split()
        counts = list(map(int, countstr.split(",")))
        springs.append((spring, counts))


def solve(record: str, counts: list[int], depth=1) -> int:
    if not counts:
        return 1

    n_solutions = 0
    count, rest_counts = counts[0], counts[1:]

    prefix = ">" * depth + " "
    # print(f"{prefix}Solving for {record} {counts}")

    # find all positions where `count` would fit
    # print(f"{prefix}Checking starts from 0 to {len(record) - count}")
    for start in range(len(record) - count + 1):
        if any(ch == "#" for ch in record[:start]):
            # print(f"{prefix}Skipped a #, not counting any more")
            break
        end = start + count
        subrecord = record[start:end]
        # check if this spring fits
        if all(ch in "?#" for ch in subrecord):
            if end < len(record) and record[end] == "#":
                # print(f"{prefix}{count} isn't bordered right at {start} : {end}")
                continue
            if start > 0 and record[start - 1] == "#":
                # print(f"{prefix}{count} isn't bordered left at {start} : {end}")
                continue

            # print(f"{prefix}{count} fits in {start} : {end}")
            # if (count, subrecord_start, subrecord_end) == (1, 2, 3):
            #     breakpoint()
            new_subrecord = record[end + 1 :]
            n_sub_solutions = solve(new_subrecord, rest_counts, depth + 1)
            # print(f"{prefix}Found {n_sub_solutions} intermediate solutions")
            n_solutions += n_sub_solutions

    # print(f"{prefix}Found {n_solutions} solutions for {record} {counts}")
    return n_solutions


assert solve("###", [3]) == 1
assert solve("???.###", [1, 1, 3]) == 1
assert (sol := solve("?###????????", [3, 2, 1])) == 10, f"Wrong solution: {sol}"
assert (sol := solve("#??.????#??.", [2, 1, 2, 1])) == 2, f"Wrong solution: {sol}"
assert (sol := solve("??#???#?????.?", [5, 1, 1])) == 12, f"Wrong solution: {sol}"

part1 = 0
for spring in tqdm(springs):
    subp1 = solve(*spring)
    # print(spring, subp1)
    part1 += subp1
print(part1)  # 9001 too high, 7323 too high
