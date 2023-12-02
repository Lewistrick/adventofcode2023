from dataclasses import dataclass


@dataclass
class Round:
    green: int = 0
    red: int = 0
    blue: int = 0

    @classmethod
    def from_str(cls, s):
        colors = s.split(",")
        data = {}
        for colorx in colors:
            n, color = colorx.split()
            data[color.strip()] = int(n.strip())
        return cls(**data)

    def is_possible(self, rules):
        for color, n in rules.items():
            if getattr(self, color) > n:
                return False
        return True


@dataclass
class Game:
    id: int
    rounds: list[Round]

    @classmethod
    def from_line(cls, line):
        game, rounds_str = line.split(":")
        id = int(game.split(" ")[-1])
        rounds = [Round.from_str(round) for round in rounds_str.split(";")]
        return cls(id, rounds)

    def is_possible(self, rules):
        return all(round.is_possible(rules) for round in self.rounds)

    def calculate_power(self):
        minr, ming, minb = 0, 0, 0
        for round in self.rounds:
            minr = max(minr, round.red)
            ming = max(ming, round.green)
            minb = max(minb, round.blue)
        return minr * ming * minb


part1_rules = {"red": 12, "green": 13, "blue": 14}
with open("02.in") as f:
    part1 = 0
    part2 = 0
    for line in f:
        game = Game.from_line(line)
        if game.is_possible(part1_rules):
            part1 += game.id
        part2 += game.calculate_power()
    print(part1)
    print(part2)
