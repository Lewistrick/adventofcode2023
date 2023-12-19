import copy
from dataclasses import dataclass


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    @classmethod
    def from_line(cls, line: str):
        line = line[line.index("{") + 1 : line.index("}")]
        values = {}
        for sub in line.split(","):
            k, v = sub.split("=")
            values[k] = int(v)
        return cls(**values)

    @property
    def rating(self):
        return self.x + self.m + self.a + self.s


@dataclass
class Workflow:
    name: str
    rules: str | list[tuple[str, str, int, str]]

    @classmethod
    def from_line(cls, line: str):
        name, rest = line.split("{")
        rest = rest.strip().strip("}")
        rules = []
        for sub in rest.split(","):
            if ":" in sub:
                r, tgt = sub.split(":")
                rules.append((r[0], r[1], int(r[2:]), tgt))
            else:
                rules.append(sub)
        return cls(name=name, rules=rules)

    def apply(self, part: Part):
        for rule in self.rules:
            if isinstance(rule, str):
                return rule
            check, comp, value, tgt = rule
            if comp == ">" and getattr(part, check) > value:
                return tgt
            if comp == "<" and getattr(part, check) < value:
                return tgt
        raise ValueError("No rule applied?")


class WorkflowNode:
    def __init__(self, name, x, m, a, s):
        self.name = name
        self.x: range = x
        self.m: range = m
        self.a: range = a
        self.s: range = s
        self.children: list["WorkflowNode"] = []

    def create_children(self, workflows: dict[str, Workflow]):
        if self.name in ("A", "R"):
            return
        fallback_ranges = {
            "x": range(self.x.start, self.x.stop),
            "m": range(self.m.start, self.m.stop),
            "a": range(self.a.start, self.a.stop),
            "s": range(self.s.start, self.s.stop),
        }
        # iterate over all workflows, except the last one (this is the fallback)
        for check, comp, value, tgt in workflows[self.name].rules[:-1]:
            child_ranges = copy.deepcopy(fallback_ranges)
            # example: check=s comp=> value=2770 tgt=qs
            if comp == ">":
                # if s>2770 then go to qs
                # let's say qs.s is [2000..3000]
                # - then the new range should become [2771..3000]
                # let's say fallback.s is [2000..3000]
                # - then the new range should become [2000..2770]
                child_ranges[check] = range(value + 1, child_ranges[check].stop)
                fallback_ranges[check] = range(fallback_ranges[check].start, value)
            # example: check=a comp=< value=2006 tgt=qkq
            elif comp == "<":
                # if a<2006 then go to qkq
                # let's say qkq.a is [2000..3000]
                # - then the new range should become [2000..2005]
                # let's say fallback.a is [2000..3000]
                # - then the new range should become [2006..3000]
                child_ranges[check] = range(child_ranges[check].start, value - 1)
                fallback_ranges[check] = range(value, fallback_ranges[check].stop)

            child = WorkflowNode(name=tgt, **child_ranges)
            child.create_children(workflows)
            self.children.append(child)

        fallback_wf_name: Workflow = workflows[self.name].rules[-1]
        child = WorkflowNode(name=fallback_wf_name, **fallback_ranges)
        child.create_children(workflows)
        self.children.append(child)

    def calculate_accepted(self):
        if self.name == "R":
            return 0
        if self.name == "A":
            total = 1
            for ch in "xmas":
                r: range = getattr(self, ch)
                print(f"{ch}={r.stop-r.start+1}")
                total *= r.stop - r.start + 1
            print(f"Subtotal: {total}")
            return total
        return sum(child.calculate_accepted() for child in self.children)

    def show(self, depth=0):
        prefix = "--" * depth
        print(f"{prefix} {self.name}")
        for ch in "xmas":
            r: range = getattr(self, ch)
            print(f"{prefix} {ch} [{r.start}..{r.stop}]")
        for child in self.children:
            child.show(depth=depth + 1)


with open("19.in") as f:
    rules_, parts_ = f.read().split("\n\n")
    rules = rules_.split("\n")
    parts = [Part.from_line(line) for line in parts_.split("\n")]
    wfs: list[Workflow] = (Workflow.from_line(line) for line in rules_.split("\n"))

workflows: dict[str, Workflow] = {wf.name: wf for wf in wfs}

A: list[Part] = []
R: list[Part] = []
for part in parts:
    wf = workflows["in"]
    while True:
        res = wf.apply(part)
        if res == "A":
            A.append(part)
            break

        if res == "R":
            R.append(part)
            break

        wf = workflows[res]

part1 = sum(p.rating for p in A)
print(part1)

wfn = WorkflowNode(
    name="in",
    x=range(1, 4000),  # should be inclusive ranges
    m=range(1, 4000),
    a=range(1, 4000),
    s=range(1, 4000),
)
wfn.create_children(workflows)
wfn.show()
breakpoint()
part2 = wfn.calculate_accepted()
print(part2)
