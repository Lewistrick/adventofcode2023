from typing import Generator


def find_all(string: str, substring: str) -> Generator[int, None, None]:
    """Find all indices of occurrences of `substring` in `string`."""
    from_idx = 0
    while (fi := string.find(substring, from_idx)) != -1:
        yield fi
        from_idx = fi + 1


vals = {
    t: i
    for i, t in enumerate(
        ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"], 1
    )
}

tot1 = 0
tot2 = 0
with open(r"1.in.txt") as f:
    for line in f:
        digits = [(i, int(x)) for i, x in enumerate(line) if x.isdigit() and x != "0"]
        # part 1
        num1 = 10 * digits[0][1] + digits[-1][1]
        tot1 += num1

        # part 2
        words = []
        for val, j in vals.items():
            for fi in find_all(line, val):
                digits.append((fi, j))

        digits = sorted(digits)
        num = digits[0][1] * 10 + digits[-1][1]
        tot2 += num

assert tot1 == 54159
assert tot2 == 53866

print(tot1)
print(tot2)
