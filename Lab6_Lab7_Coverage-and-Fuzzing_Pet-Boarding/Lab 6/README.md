# L6_L7_49 — Pet Boarding

Lab 6: Code and Branch Coverage

## About

A small Python module that works out boarding fees by pet type, days and premium kennel, checks whether a pet can be admitted and reports checkout status.

## Files

| File | Description |
|------|-------------|
| `pet_boarding.py` | The module under test |
| `test_pet_boarding.py` | Starter test file |

Keep all your Lab 6 work in this `LAB6` folder. Lab 7 will be added to this repo later.

Refer to the lab handout for instructions.

## Lab 6 Results

| Suite | Command | Result |
|-------|---------|--------|
| `CodeCoverageTest_pet_boarding.py` (11 tests) | `coverage run -m pytest CodeCoverageTest_pet_boarding.py` | **100 % line coverage** (37/37 statements) |
| `BranchCoverageTest_pet_boarding.py` (39 tests) | `coverage run --branch -m pytest BranchCoverageTest_pet_boarding.py` | **100 % line + branch coverage** (26/26 branches) |

Starter test file alone: 32 % line coverage.

### How to run

```bash
pip install coverage pytest
cd "Lab 6"

# line coverage
coverage run -m pytest CodeCoverageTest_pet_boarding.py
coverage report -m

# branch coverage
coverage run --branch -m pytest BranchCoverageTest_pet_boarding.py
coverage report -m
```

### What each suite covers

* **Code coverage suite** - the smallest set that executes every line: both `ValueError` paths, premium cat, dog with the long-stay surcharge, senior / too-young / normal admission, and the open / late / closed checkout results. It deliberately leaves one branch (a long-stay *cat*, line 21 -> 23) unexercised, which shows why 100 % line coverage can still hide an untested path.
* **Branch coverage suite** - makes every `if` / `elif` / `and` evaluate both ways, with boundary values: `extra` = 10 vs 11, premium rabbit vs premium cat, all four checkout cutoffs (15 / 30 / 35 / 50) at `cutoff`, `cutoff-1`, `cutoff-15` and `cutoff-16`.

