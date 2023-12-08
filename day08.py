from itertools import cycle
from math import lcm

nodes: dict[str, tuple[str, str]] = {}

with open("08.in") as f:
    instructions = f.readline().strip()
    f.readline()  # empty
    for line in f:
        node, lr = line.strip().split(" = (")
        left, right = lr.strip(")").split(", ")
        nodes[node] = (left, right)


def get_cycle_length(nodes, instructions, currnode, end_determiner):
    for ii, instruction in enumerate(cycle(instructions), 1):
        left, right = nodes[currnode]
        match instruction:
            case "L":
                currnode = left
            case "R":
                currnode = right
            case _:
                raise ValueError("x")
        if end_determiner(currnode):
            return ii


def end_determiner_p1(node: str):
    return node == "ZZZ"


currnode = "AAA"
part1 = get_cycle_length(nodes, instructions, currnode, end_determiner_p1)
print(part1)


def end_determiner_p2(node: str):
    return node.endswith("Z")


curr_nodes = [node for node in nodes.keys() if node.endswith("A")]
cycle_lengths = []
for node in curr_nodes:
    cycle_lengths.append(
        get_cycle_length(
            nodes,
            instructions,
            node,
            end_determiner_p2,
        )
    )

# Two big assumptions here:
# - every cycle only contains only one **Z
# - every cycle length is a multiple of the instructions length
print(lcm(*cycle_lengths))
