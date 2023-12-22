from collections import defaultdict
from dataclasses import dataclass
from itertools import count
from typing import DefaultDict


@dataclass
class Brick:
    name: str
    xrange: range
    yrange: range
    zrange: range

    def __hash__(self):
        return hash(self.xrange) ^ hash(self.yrange) ^ hash(self.zrange)

    @classmethod
    def from_line(cls, line: str, name: str):
        f, t = line.strip().split("~")
        rngs: list[range] = []
        for s, e in zip(map(int, f.split(",")), map(int, t.split(","))):
            rngs.append(range(min(s, e), max(s, e) + 1))
        return cls(name, *rngs)

    @property
    def lowest(self):
        return self.zrange.start

    def rests_on(self, other: "Brick") -> bool:
        for x in self.xrange:
            for y in self.yrange:
                if x in other.xrange and y in other.yrange:
                    return True
        return False

    def drop(self, heights: DefaultDict[int, list["Brick"]]):
        print(f"Dropping {self.name}")

        if self.lowest == 1:
            return False

        # find all stones below
        below = [stone for stone in heights[self.lowest - 1] if stone != self]

        for other in below:
            if self.rests_on(other):
                print(f"{self.name} rests on {other.name}")
                return False

        # This brick doesn't rest on any other brick!

        for z in self.zrange:
            heights[z].remove(self)
            heights[z - 1].append(self)
        self.zrange = range(self.zrange.start - 1, self.zrange.stop - 1)

        ndropped = 1
        # Check if the brick can drop any further
        while self.drop(heights):
            ndropped += 1

        print(f"Dropped {ndropped} times")
        return True


bricks: list[Brick] = []
heights: DefaultDict[int, list[Brick]] = defaultdict(list)  # height: [bricks]
# names = product(ascii_uppercase, ascii_uppercase, ascii_uppercase)
names = (f"{i:04d}" for i in count(1))
with open("22.in") as f:
    for line, name in zip(f, names):
        brick = Brick.from_line(line, "".join(name))
        bricks.append(brick)
        for z in brick.zrange:
            heights[z].append(brick)

dropped: set[Brick] = set()
for h in sorted(heights):
    for brick in heights[h]:
        if brick in dropped:
            continue
        brick.drop(heights)
        dropped.add(brick)

not_dropped: set[Brick] = set(bricks) - dropped
breakpoint()
lowest_not_dropped: Brick = min(not_dropped, key=lambda b: b.lowest)

print(f"Not dropped: {lowest_not_dropped}")
breakpoint()

for h in sorted(heights):
    print(f"{h:3d}: {" ".join(b.name for b in heights[h])}")
