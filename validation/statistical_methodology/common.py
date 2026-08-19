"""Small shared helpers for the statistical validation scripts."""

from __future__ import annotations

import csv
import io
import random
import sys
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
LAMBDA_DIR = REPO_ROOT / "lambda"
RESULTS_DIR = SCRIPT_DIR / "results"

if str(LAMBDA_DIR) not in sys.path:
    sys.path.insert(0, str(LAMBDA_DIR))

from list_generation.generate_list import generate_blocks  # noqa: E402


REPORTED_GROUPS = {"A": 5, "B": 5, "C": 2}
REPORTED_BLOCK_SIZES = (12, 24)
REPORTED_LIST_LENGTH = 240


def generate_rows(
    seed: int,
    treatment_groups: Mapping[str, int],
    block_sizes: Sequence[int],
    list_length: int,
) -> list[dict[str, object]]:
    """Call the production generator with an explicit seed and no debug output."""

    previous_state = random.getstate()
    try:
        random.seed(seed)
        with redirect_stdout(io.StringIO()):
            rows = generate_blocks(
                list(block_sizes),
                list_length,
                dict(treatment_groups),
            )
    finally:
        random.setstate(previous_state)

    return rows


def groups_from_rows(rows: Iterable[Mapping[str, object]]) -> list[str]:
    return [str(row["group"]) for row in rows]


def target_proportions(treatment_groups: Mapping[str, int]) -> dict[str, float]:
    total = sum(treatment_groups.values())
    return {group: weight / total for group, weight in treatment_groups.items()}


def expected_block_counts(
    treatment_groups: Mapping[str, int], block_size: int
) -> dict[str, int]:
    groups = list(treatment_groups)
    weights = np.asarray(list(treatment_groups.values()), dtype=float)
    counts = np.rint(weights / weights.sum() * block_size).astype(int)
    return dict(zip(groups, counts, strict=True))


def observed_blocks(rows: Iterable[Mapping[str, object]]) -> dict[int, Counter[str]]:
    blocks: dict[int, Counter[str]] = defaultdict(Counter)
    for row in rows:
        blocks[int(row["block_index"])][str(row["group"])] += 1
    return dict(blocks)


def summarize(values: Sequence[float]) -> dict[str, float]:
    array = np.asarray(values, dtype=float)
    return {
        "mean": float(np.mean(array)),
        "sd": float(np.std(array, ddof=1)) if len(array) > 1 else 0.0,
        "min": float(np.min(array)),
        "p2_5": float(np.quantile(array, 0.025)),
        "median": float(np.quantile(array, 0.5)),
        "p97_5": float(np.quantile(array, 0.975)),
        "max": float(np.max(array)),
    }


def write_csv(path: Path, fieldnames: Sequence[str], rows: Iterable[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

