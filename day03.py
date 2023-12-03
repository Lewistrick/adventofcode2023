from collections import defaultdict
import math

nums = {}
parts = {}

with open("03.in") as lines:
    for li, line in enumerate(lines):
        currnum = ""
        for ci, ch in enumerate(line.strip()):
            if ch.isdigit():
                currnum += ch
                continue
            elif ch != ".":
                # it's a part
                parts[(li, ci)] = ch
            if currnum:
                nums[(li, ci - 1)] = int(currnum)
                currnum = ""
        if currnum:
            nums[(li, ci)] = int(currnum)

part1 = 0
lastline = -1
gears_touched = defaultdict(list)
for (num_li, num_ci1), num in nums.items():
    if lastline != num_li and lastline != -1:
        print()
    lastline = num_li

    num_ci0 = num_ci1 - int(math.log(num, 10))
    # check if touches part
    touched_parts = []
    for ci in range(num_ci0 - 1, num_ci1 + 2):
        for li in (num_li - 1, num_li, num_li + 1):
            if (li, ci) in parts:
                touched_part = parts[(li, ci)]
                touched_parts.append((touched_part, li, ci))
                if touched_part == "*":
                    # gear touched!
                    gears_touched[(li, ci)].append(num)
            if num == 92:
                print(f"Checked: {(li, ci)}")
    if touched_parts:
        print(f"{num} touched {touched_parts}", end=" / ")
        part1 += num
    else:
        print(f"{num} doesn't touch any parts", end=" / ")
        # input()
    print(f"Total: {part1}")

print(part1)
# 519922 too low
# 521740 too high
# 521601 correct

part2 = 0
for gear, touches in gears_touched.items():
    if len(touches) == 1:
        continue

    n1, n2 = touches
    part2 += n1 * n2
print(part2)
