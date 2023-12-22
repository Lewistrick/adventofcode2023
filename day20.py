Node = tuple[str, tuple[str], bool]
Nodes = dict[str, Node]
ConjuctionMemory = dict[str, dict[str, bool]]


def traverse(nodes: Nodes, start: str, cmem: ConjuctionMemory):
    typ, dests, state = start
    queue: list[tuple[str, bool]] = []
    if typ == "broadcaster":
        # send a low signal (False) to all nodes
        for nodename in dests:
            queue.append((nodename, False))

    cmem = {}
    while queue:
        nodename, signal = queue.pop(0)
        nodetype, dests, state = nodes[nodename]
        match nodetype, signal, state:
            case "%", True:
                continue
            case "%", False:
                # if on, send high; if off, send low
                for dest in dests:
                    queue.append(dest, not state)
                # invert state
                nodes[nodename] = (nodetype, dests, not state)
            case "&", s:
                # update memory
                cmem[nodename] = s
                # if all high, send low; else, send high
                all_high = all(cmem[nodename])
                for dest in dests:
                    queue.append(dest, not all_high)
        ...


with open("20.ex") as f:
    lines = f.read().split("\n")

nodes: Nodes = {}
for line in lines:
    name, dests = line.split(" -> ")
    if name == "broadcaster":
        typ = name
    else:
        typ, name = name[0], name[1:]
    dests = tuple(dests.split(", "))
    # state False means 'off' for %, 'low' for & and nothing for broadcaster
    nodes[name] = (typ, dests, False)

# for each & node, store last pulse from every input (initially low)
mem: ConjuctionMemory = {}
for node, (typ, dests, state) in nodes.items():
    mem[node] = {dest: False for dest in dests}

for button_press in range(1000):
    traverse(nodes, "broadcaster", mem)
