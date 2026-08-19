"""Check equal ratios, short lists, and large block sizes."""

from collections import Counter

from common import (
    RESULTS_DIR,
    expected_block_counts,
    generate_rows,
    observed_blocks,
    write_csv,
)


RUNS_PER_CASE = 100
BASE_SEED = 20260331

CASES = (
    ("reported_5_5_2", {"A": 5, "B": 5, "C": 2}, (12, 24), 240, 240),
    ("equal_two_arm", {"A": 1, "B": 1}, (4, 8), 40, 40),
    ("equal_three_arm", {"A": 1, "B": 1, "C": 1}, (3, 6), 30, 30),
    ("very_short_list", {"A": 5, "B": 5, "C": 2}, (12, 24), 5, 12),
    ("minimum_block_fit", {"A": 5, "B": 5, "C": 2}, (12, 24), 12, 12),
    ("very_large_block", {"A": 5, "B": 5, "C": 2}, (600,), 600, 600),
    ("large_block_overrun", {"A": 5, "B": 5, "C": 2}, (600,), 50, 600),
)


def check_case(groups, block_sizes, requested_length, expected_length, seed):
    rows = generate_rows(seed, groups, block_sizes, requested_length)
    assert len(rows) == expected_length
    assert {row["group"] for row in rows} <= set(groups)

    blocks = observed_blocks(rows)
    assert list(blocks) == list(range(len(blocks)))
    for counts in blocks.values():
        block_size = sum(counts.values())
        assert block_size in block_sizes
        assert counts == Counter(expected_block_counts(groups, block_size))

    return tuple(row["group"] for row in rows)


def main() -> None:
    results = []

    for case_number, case in enumerate(CASES):
        name, groups, block_sizes, requested_length, expected_length = case
        sequences = {
            check_case(
                groups,
                block_sizes,
                requested_length,
                expected_length,
                BASE_SEED + case_number * 1000 + run,
            )
            for run in range(RUNS_PER_CASE)
        }
        results.append(
            {
                "case": name,
                "status": "PASS",
                "groups": groups,
                "block_sizes": block_sizes,
                "requested_length": requested_length,
                "observed_length": expected_length,
                "runs": RUNS_PER_CASE,
                "unique_sequences": len(sequences),
            }
        )
        print(f"PASS  {name}: requested {requested_length}, observed {expected_length}")

    write_csv(
        RESULTS_DIR / "configuration_checks.csv",
        results[0].keys(),
        results,
    )


if __name__ == "__main__":
    main()

