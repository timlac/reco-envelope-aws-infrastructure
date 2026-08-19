"""Run the reported 5:5:2 design 10,000 times."""

import hashlib
import json
from collections import Counter

import numpy as np

from common import (
    REPORTED_BLOCK_SIZES,
    REPORTED_GROUPS,
    REPORTED_LIST_LENGTH,
    RESULTS_DIR,
    generate_rows,
    groups_from_rows,
    summarize,
    target_proportions,
)


RUNS = 10_000
BASE_SEED = 20260331
INTERIM_POINTS = (12, 24, 60, 120, 180, 240)


def main() -> None:
    groups = list(REPORTED_GROUPS)
    targets = target_proportions(REPORTED_GROUPS)
    group_index = {group: index for index, group in enumerate(groups)}

    final_proportions = {group: [] for group in groups}
    interim_imbalance = {point: [] for point in INTERIM_POINTS}
    position_counts = np.zeros((REPORTED_LIST_LENGTH, len(groups)), dtype=int)
    adjacent_equal_rates = []
    sequence_hashes = set()

    for run in range(RUNS):
        rows = generate_rows(
            BASE_SEED + run,
            REPORTED_GROUPS,
            REPORTED_BLOCK_SIZES,
            REPORTED_LIST_LENGTH,
        )
        sequence = groups_from_rows(rows)
        assert len(sequence) == REPORTED_LIST_LENGTH

        sequence_hashes.add(
            hashlib.sha256(json.dumps(sequence).encode()).hexdigest()
        )

        for position, group in enumerate(sequence):
            position_counts[position, group_index[group]] += 1

        adjacent_equal_rates.append(
            sum(a == b for a, b in zip(sequence, sequence[1:]))
            / (len(sequence) - 1)
        )

        final_counts = Counter(sequence)
        for group in groups:
            final_proportions[group].append(final_counts[group] / len(sequence))

        for point in INTERIM_POINTS:
            counts = Counter(sequence[:point])
            deviations = [
                abs(counts[group] - point * targets[group]) for group in groups
            ]
            interim_imbalance[point].append(max(deviations))

    target_array = np.array([targets[group] for group in groups])
    position_proportions = position_counts / RUNS
    position_deviations = np.abs(position_proportions - target_array)

    result = {
        "design": {
            "runs": RUNS,
            "base_seed": BASE_SEED,
            "treatment_groups": REPORTED_GROUPS,
            "block_sizes": REPORTED_BLOCK_SIZES,
            "list_length": REPORTED_LIST_LENGTH,
        },
        "final_proportions": {
            group: {"target": targets[group], **summarize(values)}
            for group, values in final_proportions.items()
        },
        "interim_maximum_absolute_group_deviation": {
            str(point): summarize(values)
            for point, values in interim_imbalance.items()
        },
        "randomness_diagnostics": {
            "unique_sequences": len(sequence_hashes),
            "duplicate_sequences": RUNS - len(sequence_hashes),
            "maximum_position_target_deviation": float(position_deviations.max()),
            "mean_position_target_deviation": float(position_deviations.mean()),
            "adjacent_equal_assignment_rate": summarize(adjacent_equal_rates),
            "independent_assignment_reference": sum(
                proportion**2 for proportion in targets.values()
            ),
        },
    }

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "simulation_summary.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    print(f"Completed {RUNS:,} simulations: {RESULTS_DIR / 'simulation_summary.json'}")


if __name__ == "__main__":
    main()
