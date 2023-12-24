# typehints
from typing import Literal

Pos = tuple[int, int]
Placement = Literal[-1, 0, 1]
DirectionTuple = tuple[Placement, Placement]

# directions (both relative (right/left/up/down) and absolute (east/west/north/south))
ddir: dict[str, DirectionTuple] = {
    "U": (0, -1),
    "R": (1, 0),
    "D": (0, 1),
    "L": (-1, 0),
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0),
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}

DIRS4 = tuple(ddir[d] for d in "NESW")
