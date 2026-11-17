# L6_L7_49 — Pet Boarding

Lab 7: Fuzz Testing

## About

A small Python module that parses boarding bookings, averages stay lengths and works out the payable fee after a discount.

## Files

| File | Description |
|------|-------------|
| `pet_boarding.py` | The code under test |
| `test_pet_boarding.py` | Starter test file |

Refer to the lab handout for instructions.

## Lab 7 Results

Fuzzing with Hypothesis found that all three functions crashed or misbehaved on bad input:

| Function | Bugs found by fuzzing | Fix |
|----------|----------------------|-----|
| `parse_booking` | `None` -> `AttributeError`; no `:` / extra `:` / empty days -> `ValueError`; accepted `nan`, `inf`, `1e999`, negative days and an empty pet name | Type check, exactly one `:`, non-empty pet, days must be finite and >= 0 |
| `stay_average` | `None` -> `AttributeError`; `''`, `1,,3`, `a,b`, `1.5` -> `ValueError`; negative stays accepted | Type check, every item must be a whole number >= 0 |
| `payable_fee` | `None` -> `AttributeError`; missing / extra `|` -> `ValueError`; `nan` / `inf` fee or discount accepted (returned `nan`), negative fee / discount accepted (a negative discount *raised* the bill) | Type check, exactly one `|`, both values finite and >= 0, result must be finite |

Design: invalid input now returns `None` (no exception); `main()` prints a clear message.
Valid inputs behave exactly as before. Note: `stay_average` still uses integer (floor) division, as in the original.

| Step | Before (buggy) | After (fixed) |
|------|----------------|---------------|
| `pytest test_pet_boarding.py` | 63 failed, 14 passed | **77 passed** |

### How to run

```bash
pip install hypothesis pytest
cd "Lab 7"
python pet_boarding.py
python -m pytest test_pet_boarding.py
```

