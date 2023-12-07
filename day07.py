from collections import Counter

hands = []


with open("07.in") as lines:
    for line in lines:
        hands.append(line.strip().split())


def get_hand_score(hand, jokers=False):
    """Return a number to sort the hand type by.

    Five of a kind returns the highest score, high card the lowest.
    If jokers==True, add the number of J's to the count of the most-occurring card
    """
    ctr = Counter(hand)
    if jokers and "J" in ctr:
        njokers = ctr.pop("J")
        # if a hand is all jokers, we can't add it to any other card
        if njokers == 5:
            return 7
        ((most_common_card, n),) = ctr.most_common(1)
        n += njokers
        ctr[most_common_card] = n
    cts = [card[-1] for card in ctr.most_common()]

    if cts[0] == 5:
        return 7  # five of a kind
    if cts[0] == 4:
        return 6  # four of a kind
    if cts[0] == 3 and cts[1] == 2:
        return 5  # full house
    if cts[0] == 3:
        return 4
    if cts[0] == 2 and cts[1] == 2:
        return 3  # two pair
    if cts[0] == 2:
        return 2  # one pair
    if cts[0] == 1:
        return 1  # high card


cvalues = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}


def get_cards(hand, cvalues=cvalues):
    values = []
    for card in hand:
        try:
            value = int(card)
        except:
            value = cvalues[card]
        values.append(value)
    return tuple(values)


# The best part of sorting is that it can take a key to sort by; the key determines
# for two hands which is higher (using the < operator).
# So we define the key as a (hand_type, values) tuple. It first compares by hand_type
# (five of a kind being highest) and then by values (the numeric values of the cards).
hands = sorted(
    hands,
    key=lambda hand: tuple(
        (
            get_hand_score(hand[0]),
            get_cards(hand[0]),
        ),
    ),
)

# Sorting is done worst-to-best so we can just give rank 1 to the worst hand
part1 = 0
for i, (hand, bid) in enumerate(hands, 1):
    part1 += i * int(bid)
print(part1)

# Same trick, but then make sure the key takes jokers into account
cvalues2 = cvalues.copy()
cvalues2["J"] = 1
hands2 = sorted(
    hands,
    key=lambda hand: tuple(
        (
            get_hand_score(hand[0], jokers=True),
            get_cards(hand[0], cvalues2),
        )
    ),
)

part2 = 0
for i, (hand, bid) in enumerate(hands2, 1):
    part2 += i * int(bid)
print(part2)
