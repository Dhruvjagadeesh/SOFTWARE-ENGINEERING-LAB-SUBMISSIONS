# L6_L7_49 - Pet Boarding

Software Engineering lab work (Labs 6 and 7) on a small Pet Boarding Python project.

**Name:** Dhruv Jagadeesh Hemmige
**SRN:** PES2UG24AM053

## Repository structure

```
.
|-- Lab 6/                                 Code and branch coverage analysis
|   |-- pet_boarding.py                    Module under test (fees, admission, checkout)
|   |-- test_pet_boarding.py               Starter tests
|   |-- CodeCoverageTest_pet_boarding.py   Tests for line (code) coverage
|   |-- BranchCoverageTest_pet_boarding.py Tests for branch coverage
|   |-- screenshots/                       Coverage report screenshots
|   `-- README.md
|-- Lab 7/                                 Fuzzing for input validation bugs
|   |-- pet_boarding.py                    Hardened booking parsers
|   |-- test_pet_boarding.py               Hypothesis fuzz tests
|   |-- Lab7_Fuzzing_Report.pdf            Report with before / after screenshots
|   `-- README.md
`-- README.md
```

## Setup

Requires Python 3.8+.

```bash
pip install coverage pytest hypothesis
```

## Lab 6 - Code and Branch Coverage

Goal: measure coverage with `coverage.py` and write tests that exercise every line and every decision branch of `pet_boarding.py`.

```bash
cd "Lab 6"

# line coverage
coverage run -m pytest CodeCoverageTest_pet_boarding.py
coverage report -m

# branch coverage
coverage run --branch -m pytest BranchCoverageTest_pet_boarding.py
coverage report -m
```

| Suite | Tests | Result |
|-------|-------|--------|
| `CodeCoverageTest_pet_boarding.py` | 11 | 100 % line coverage (37/37 statements) |
| `BranchCoverageTest_pet_boarding.py` | 39 | 100 % branch coverage (26/26 branches) |

The starter test file alone reached 32 % line coverage.

## Lab 7 - Fuzzing for Input Validation Bugs

Goal: use property-based fuzzing (Hypothesis) to find input validation bugs in `parse_booking`, `stay_average` and `payable_fee`, then fix them.

```bash
cd "Lab 7"
python pet_boarding.py
python -m pytest test_pet_boarding.py
```

| Stage | Result |
|-------|--------|
| Original code | 63 failed, 14 passed |
| Hardened code | 77 passed |

Bugs found by fuzzing included crashes on `None`, empty strings and missing or extra separators, plus silently accepted `nan`, `inf` and negative values. The fixed functions return `None` for invalid input and `main()` prints a clear message. See `Lab 7/README.md` and `Lab7_Fuzzing_Report.pdf` for details.
