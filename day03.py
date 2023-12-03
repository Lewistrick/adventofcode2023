from collections import defaultdict
import math

# save parts as {coordinate: part}
parts = {}
# save numbers as {coordinate: num}, where the *last* digit of a number is stored
nums = {}

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
        # Forgot this first: if a num is at the end of a line, it should be added.
        # Note that the -1 is omitted here because ci is part of the number
        if currnum:
            nums[(li, ci)] = int(currnum)

part1 = 0
lastline = -1
gears_touched = defaultdict(list)
for (num_li, num_ci1), num in nums.items():
    # if lastline != num_li and lastline != -1:
    #     print()
    lastline = num_li

    # Find the coordinate of the first digit of the number
    num_ci0 = num_ci1 - int(math.log(num, 10))

    # Check if the number touches a part
    touched_parts = False
    for ci in range(num_ci0 - 1, num_ci1 + 2):
        for li in (num_li - 1, num_li, num_li + 1):
            if (li, ci) in parts:
                touched_parts = True
                touched_part = parts[(li, ci)]
                # Check if the touched part is a gear
                if touched_part == "*":
                    gears_touched[(li, ci)].append(num)
    if touched_parts:
        part1 += num

print(part1)

part2 = 0
for gear, touches in gears_touched.items():
    if len(touches) == 1:
        continue

    n1, n2 = touches  # assumes that a gear is touched by at most 2 numbers
    part2 += n1 * n2

print(part2)
