from typing import Generator

tot = 0
with open(r"1.in.txt") as f:
    for line in f:
        digits = [x for x in line if x.isdigit()]
        num = int(digits[0] + digits[-1])
        tot += num
print(tot)

### PART 2
vals = {
    t: i
    for i, t in enumerate(
        ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"], 1
    )
}


def find_all(string: str, substring: str) -> Generator[int, None, None]:
    from_idx = 0
    while (fi := string.find(substring, from_idx)) != -1:
        yield fi
        from_idx = fi + 1


tot2 = 0
with open(r"1.in.txt") as f:
    for line in f:
        digits = [(i, int(x)) for i, x in enumerate(line) if x.isdigit() and x != "0"]
        words = []
        for val, j in vals.items():
            for fi in find_all(line, val):
                digits.append((fi, j))

        digits = sorted(digits)

        num = digits[0][1] * 10 + digits[-1][1]
        tot2 += num

print(tot2)  # fout: 55379, 53859, 54296
# goed: 53866
