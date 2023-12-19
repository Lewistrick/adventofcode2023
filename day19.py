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


with open("19.in") as f:
    rules_, parts_ = f.read().split("\n\n")
    rules = rules_.split("\n")
    parts = [Part.from_line(line) for line in parts_.split("\n")]
    wfs: list[Workflow] = (Workflow.from_line(line) for line in rules_.split("\n"))

workflows = {wf.name: wf for wf in wfs}

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
