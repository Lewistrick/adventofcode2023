from collections import defaultdict


def parse_line(line):
    gameid, nums = line.split(": ")
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
    print("-" * 80)
    print(f"{gameid=}")
    score = scores[gameid]
    print(f"Score of this game: {score}")
    ncopies = copies[gameid] + 1
    print(f"This game has {ncopies} copies (including the original)")
    for i in range(gameid + 1, gameid + score + 1):
        print(f"Adding {ncopies} copies of game {i}")
        copies[i] += ncopies
    print(sorted(copies.items()))
    part2 += ncopies
    print(f"New total: {part2}")

print(part1)
print(part2)  # to do
