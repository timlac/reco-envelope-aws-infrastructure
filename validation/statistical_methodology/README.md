# Statistical methodology validation

Three short scripts address the reviewer's statistical-methodology comments. All settings are hardcoded near the top of each script.

1. `01_simulate_reported_design.py` runs the 5:5:2 design 10,000 times and summarizes final proportions, interim imbalance, and simple randomness diagnostics.
2. `02_check_additional_configurations.py` checks equal ratios, short lists, and large blocks.
3. `03_check_reproducibility.py` compares two independent runs in Python 3.10 and Python 3.12. `seeded_sequence.py` is its small subprocess helper.

All scripts call the production function in `lambda/list_generation/generate_list.py`.

Run from the repository root:

```bash
.venv/bin/python validation/statistical_methodology/01_simulate_reported_design.py
.venv/bin/python validation/statistical_methodology/02_check_additional_configurations.py
.venv/bin/python validation/statistical_methodology/03_check_reproducibility.py
```

Results are written to three files in `validation/statistical_methodology/results/`: `simulation_summary.json`, `configuration_checks.csv`, and `reproducibility_check.json`.

The production API does not accept a seed. The validation helper sets Python's random seed immediately before calling the production function. The Python 3.10/3.12 comparison uses separate interpreters on the same host and should not be described as validation across independent machines.
