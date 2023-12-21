from collections import defaultdict

with open("15.in") as f:
    data = f.read().strip().split(",")


def hash_text(text: str) -> int:
    currval = 0
    for ch in text:
        currval += ord(ch)
        currval *= 17
        currval %= 256
    return currval


part1 = 0
for s in data:
    part1 += hash_text(s)

print(part1)

boxes = defaultdict(dict)  # {box_no : {label : strength}}
for s in data:
    if "=" in s:
        label, focal_length = s.split("=")
        box_no = hash_text(label)
        # if the lens already exists, this will update the focal length
        # if it doesn't exist, it will add it to the dictionary
        # (note that since Python 3.7 dicts keep their insertion order)
        boxes[box_no][label] = int(focal_length)
    else:
        # there will always be a '-' at the end
        label = s.removesuffix("-")
        box_no = hash_text(label)
        # remove the lens from the box (.pop returns the label but we don't need it)
        # if there doesn't exist a lens with this label, do nothing (return None)
        boxes[box_no].pop(label, None)

part2 = 0
for box_no, lenses in boxes.items():
    for lens_no, (label, focal_length) in enumerate(lenses.items(), 1):
        part2 += (box_no + 1) * lens_no * focal_length

print(part2)
