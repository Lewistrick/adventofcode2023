from collections import defaultdict


def parse_line(line):
    _, nums = line.split(": ")
    left, right = nums.split(" | ")
    win = set(map(int, left.split()))
    own = set(map(int, right.split()))
    noverlap = len(win & own)
    return noverlap


part1 = 0
scores = {}  # game: score
with open("04.in") as lines:
    for i, line in enumerate(lines, 1):
        score = parse_line(line)
        if score:
            part1 += 2 ** (score - 1)
        scores[i] = score

part2 = 0
copies = defaultdict(int)  # game: n_copies (not counting original)
for gameid in sorted(scores.keys()):
    score = scores[gameid]
    ncopies = copies[gameid] + 1
    for i in range(gameid + 1, gameid + score + 1):
        copies[i] += ncopies
    part2 += ncopies

print(part1)
print(part2)
