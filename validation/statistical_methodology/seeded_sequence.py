"""Generate one sequence with the hardcoded validation seed."""

import json
import platform

import numpy as np

from common import (
    REPORTED_BLOCK_SIZES,
    REPORTED_GROUPS,
    REPORTED_LIST_LENGTH,
    generate_rows,
)


SEED = 20260331

result = {
    "sequence": generate_rows(
        SEED,
        REPORTED_GROUPS,
        REPORTED_BLOCK_SIZES,
        REPORTED_LIST_LENGTH,
    ),
    "environment": {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "platform": platform.platform(),
    },
}

print(json.dumps(result))

