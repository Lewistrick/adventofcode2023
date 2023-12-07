from typing import Optional


with open("05.in") as f:
    line = f.readline().strip()
    seeds = map(int, line.removeprefix("seeds: ").split())
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
            dst_start, srt_start, rlen = map(int, line.split())
            maps[(mfrom, mto)].append(
                (
                    range(srt_start, srt_start + rlen),
                    range(dst_start, dst_start + rlen),
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
    seed_ranges.append(range(seed_from, rng_length))

curr = "seed"
curr_rngs = seed_ranges.copy()
while curr != "location":
    map_idx = next((f, t) for (f, t) in maps.keys() if f == curr)
    prev, curr = map_idx
    map_ = maps[map_idx]
    new_rngs = []
    for curr_rng in curr_rngs:
        curr_num = curr_rng[0]
        while curr_num < curr_rng[-1]:
            # for this number, find the range it is in
            # find the upper limit of this range
            # add the range to new_rngs
            ...
            # if it's not found, find the first range that applies
            #
