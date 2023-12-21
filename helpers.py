# typehints
from typing import Literal

Pos = tuple[int, int]
Placement = Literal[-1, 0, 1]
DirectionTuple = tuple[Placement, Placement]

# directions (both relative (right/left/up/down) and absolute (east/west/north/south))
ddir: dict[str, DirectionTuple] = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, -1),
    "D": (0, 1),
    "E": (1, 0),
    "W": (-1, 0),
    "N": (0, -1),
    "S": (0, 1),
}

DIRS4 = tuple(ddir[d] for d in "NESW")
