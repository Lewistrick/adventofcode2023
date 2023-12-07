from typing import Optional

with open("05.in") as f:
    line = f.readline().strip()
    seeds = list(map(int, line.removeprefix("seeds: ").split()))
    next(f)

    maps: dict[tuple[str, str], list[tuple[range, range]]] = {}
    mfrom, mto = "", ""
    for line in f:
        if line.strip().endswith(" map:"):
            cline = line.strip().removesuffix(" map:")
            mfrom, _, mto = cline.split("-")
            maps[(mfrom, mto)] = []
        elif not line.strip():
            continue
        else:
            tgt_start, src_start, rlen = map(int, line.split())
            maps[(mfrom, mto)].append(
                (
                    range(src_start, src_start + rlen),
                    range(tgt_start, tgt_start + rlen),
                )
            )

part1: Optional[int] = None
for seed in seeds:
    # print(f"Seed: {seed}")
    curr = "seed"
    currnum = seed
    while curr != "location":
        map_idx = next((f, t) for (f, t) in maps.keys() if f == curr)
        _, curr = map_idx
        map_ = maps[map_idx]
        try:
            rngs: tuple[range] = next((f, t) for (f, t) in map_ if currnum in f)
        except StopIteration:
            # print(f"* {curr}: {currnum}")
            continue

        frng, trng = rngs
        idx = frng.index(currnum)
        currnum = trng[idx]
        # print(f"- {curr}: {currnum}")

    if part1 is None or currnum < part1:
        part1 = currnum

print(part1)


### part 2
seed_ranges = []
for seed_from, rng_length in zip(seeds[::2], seeds[1::2]):
    seed_ranges.append(range(seed_from, seed_from + rng_length))


def ranges_to_ranges(from_ranges: list[range], mappers: list[tuple[range, range]]):
    """Map ranges to new ranges.

    Example:
        from_ranges is [range(10, 100)]
        mappers consists of the following range tuples:
            - range( 0,  20) -> range(230, 250)
            - range(30,  70) -> range(100, 140)
            - range(70, 160) -> range(  0,  90)

    - The while loop will loop over all ranges in from_ranges
    - In this case the only one is range(10, 100)
    - Take the first number: 10
        - This fits in range(0, 20) [this is called `map_from`]
        - The upper limit of this range is 20
        - The range to convert becomes range(10, 20)
        - The translation adds 230-0=230 to the current range [this is called `delta`]
        - The converted range becomes range(240, 250) [this is called `to_range`]
    - Skip to the next unconverted number, which is `map_from.stop`: 20
        - This doesn't fit in any range
        - The first range above 20 is range(30, 70)
        - Create a new `to_range`: range(20, 30)
    - Skip to the next unconverted number, which is `to_range.stop`: 30
        - map_from = range(30, 70)
        - to_convert = range(30, 70)
        - delta = 70
        - to_range = range(100, 140)
    - next_unconverted = map_from.stop = 70
        - map_from = range(70, 160)
        - to_convert = range(70, 100)
        - delta = -70
        - to_range = range(0, 30)
    - Final ranges: [range(240, 250), range(20, 30), range(100, 140), range(0, 30)]
    """
    to_ranges = []
    for from_range in from_ranges:
        print()
        print(f"{from_range=}")
        next_unconverted = from_range.start
        while next_unconverted < from_range.stop:
            print(f"{next_unconverted=}")
            try:
                # find the range it's in
                map_from, map_to = next(
                    (range_from, range_to)
                    for range_from, range_to in mappers
                    if next_unconverted in range_from
                )
            except StopIteration:
                # no range found, find the next map above this
                range_above_found = False
                try:
                    first_range_above = min(
                        (
                            range_from
                            for range_from, range_to in mappers
                            if range_from.start > next_unconverted
                        ),
                        key=lambda r: r.start,
                    )
                    range_above_found = True
                except ValueError:
                    # no range found above next_unconverted
                    range_above_found = False
                if range_above_found:
                    map_from = range(next_unconverted, first_range_above.start)
                else:
                    map_from = range(next_unconverted + 1, from_range.stop)
                map_to = map_from

            print(f"{map_from=} {map_to=}")
            delta = map_to.start - map_from.start
            print(f"{delta=}")
            to_convert = range(
                max(map_from.start, next_unconverted),
                min(map_from.stop, from_range.stop),
            )
            print(f"Range to convert: {to_convert}")
            to_range = range(to_convert.start + delta, to_convert.stop + delta)
            print(f"Converted range: {to_range}")
            to_ranges.append(to_range)
            next_unconverted = to_convert.stop
            print(f"{next_unconverted=}")
    return to_ranges


curr = "seed"
curr_rngs = seed_ranges.copy()
print(curr_rngs)
while curr != "location":
    print("-" * 80)
    print(curr)
    map_idx = next((f, t) for (f, t) in maps.keys() if f == curr)
    prev, curr = map_idx
    map_ = maps[map_idx]
    # curr_rngs = sorted(ranges_to_ranges(curr_rngs, map_), key=lambda r: r.start)
    curr_rngs = ranges_to_ranges(curr_rngs, map_)
    print(curr)
    for r in curr_rngs:
        print(r)

part2 = min(r[0] for r in curr_rngs)
print(part2)
