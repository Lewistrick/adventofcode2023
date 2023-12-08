from itertools import cycle
from math import lcm
from typing import Callable

# parse input
nodes: dict[str, tuple[str, str]] = {}

with open("08.in") as f:
    instructions = f.readline().strip()
    f.readline()  # empty
    for line in f:
        node, lr = line.strip().split(" = (")
        left, right = lr.strip(")").split(", ")
        nodes[node] = (left, right)


def get_cycle_length(node: str, end_determiner: Callable[[str], bool]):
    """Get the number of steps to get from currnode to the end."""
    for ii, instruction in enumerate(cycle(instructions), 1):
        left, right = nodes[node]
        node = left if instruction == "L" else right
        if end_determiner(node):
            return ii


curr_nodes = [node for node in nodes.keys() if node.endswith("A")]
cycle_lengths = []
for node in curr_nodes:
    node_cycle_length = get_cycle_length(
        node=node,
        end_determiner=lambda node: node.endswith("Z"),
    )
    if node == "AAA":
        part1 = node_cycle_length
    cycle_lengths.append(node_cycle_length)

# Two big assumptions here:
# - every cycle only contains only one **Z node, which it ends with
# - every cycle length is a multiple of the instructions length
part2 = lcm(*cycle_lengths)

print(part1)
print(part2)
