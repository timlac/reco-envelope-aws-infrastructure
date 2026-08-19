"""Compare seeded output across independent Python processes."""

import hashlib
import json
import subprocess
from pathlib import Path

from common import REPO_ROOT, RESULTS_DIR, SCRIPT_DIR


PYTHON_ENVIRONMENTS = {
    "python_3_10": REPO_ROOT / ".venv" / "bin" / "python",
    "python_3_12": Path("/usr/bin/python3"),
}
SEQUENCE_SCRIPT = SCRIPT_DIR / "seeded_sequence.py"


def run_once(python):
    output = subprocess.check_output(
        [str(python), str(SEQUENCE_SCRIPT)],
        cwd=REPO_ROOT,
        text=True,
    )
    return json.loads(output)


def sequence_hash(result):
    sequence = json.dumps(result["sequence"], sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(sequence.encode()).hexdigest()


def main() -> None:
    results = {}

    for name, python in PYTHON_ENVIRONMENTS.items():
        assert python.exists(), f"Python executable not found: {python}"
        first = run_once(python)
        second = run_once(python)
        first_hash = sequence_hash(first)
        second_hash = sequence_hash(second)
        assert first_hash == second_hash

        results[name] = {
            "status": "PASS",
            "sequence_sha256": first_hash,
            "environment": first["environment"],
        }
        print(f"PASS  independent runs in {name}")

    hashes = {result["sequence_sha256"] for result in results.values()}
    assert len(hashes) == 1
    print("PASS  sequence matches across the two Python environments")

    report = {
        "cross_environment_status": "PASS",
        "same_host": True,
        "environments": results,
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    (RESULTS_DIR / "reproducibility_check.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()

