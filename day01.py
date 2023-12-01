from typing import Generator


def find_all(
    string: str,
    substring: str,
    from_idx: int = 0,
) -> Generator[int, None, None]:
    """Find all indices of occurrences of `substring` in `string`."""

    while (find_index := string.find(substring, from_idx)) != -1:
        yield find_index
        from_idx = find_index + 1


num_words = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
vals = {t: i for i, t in enumerate(num_words, 1)}  # {"one": 1, "two": 2, ...}

part1 = 0
part2 = 0
with open("1.in.txt") as handle:
    for line in handle:
        # part 1: find all numeric digits
        digits = [(i, int(x)) for i, x in enumerate(line) if x.isdigit()]
        num1 = 10 * digits[0][1] + digits[-1][1]
        part1 += num1

        # part 2: also find all number words
        words = []
        for val, j in vals.items():
            for fi in find_all(line, val):
                digits.append((fi, j))

        digits = sorted(digits)
        num2 = digits[0][1] * 10 + digits[-1][1]
        part2 += num2

print(part1)
print(part2)
