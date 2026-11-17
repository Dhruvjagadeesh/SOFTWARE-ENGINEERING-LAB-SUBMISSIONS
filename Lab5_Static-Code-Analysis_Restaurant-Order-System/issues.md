# Lab 5 – Issues Found and Fixed

**Name:** Dhruv Jagadeesh Hemmige  **SRN:** PES2UG24AM053
**File:** `restaurant_order_system.py`  (original line numbers)

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Weak MD5 hash (B324) | Security – High | 47 | `hashlib.md5` is cryptographically broken; ticket IDs could be forged/collided | Switched to `hashlib.sha256` |
| Shell command injection (B605) | Security – High | 58 | `os.system("echo ... " + filename)` passes user-controlled `filename` to a shell | Removed `os.system`; use `print()` and `os.path.basename()` on the filename |
| Use of `eval` (B307 / W0123) | Security – Medium | 42 | `eval(promo_expr)` executes arbitrary code supplied as the "promo expression" | `calculate_discounted_bill` now takes a numeric `discount_rate` (validated 0–1); no code execution |
| Insecure RNG for PIN (B311) | Security – Low | 51 | `random.randint` is predictable, but used to make a POS PIN | Replaced with `secrets.randbelow` |
| Hardcoded secret | Security – Medium (manual) | 71, 80 | POS token stored in source and printed to console | Read from `POS_TERMINAL_KEY` env var; only print whether it is configured |
| Try/except/pass + bare except (B110, E722, W0702) | Bug / Security | 24-27 | Swallows every error silently; caller can't tell if the void worked | Catch only `KeyError`; return `True`/`False` |
| Mutable default argument (W0102) | Bug | 15 | `order_log=[]` is shared across calls, so logs leak between orders | Default to `None`, create a new list inside the function |
| Unclosed file / no encoding (R1732, W1514) | Bug | 55-57 | `open()` without `with`; file leaks if `write` raises. Also dumps `str(dict)`, not a parseable format | `with open(..., encoding="utf-8")` and `json.dump` |
| Unused variables / import (F401, F841, W0611, W0612) | Style / Dead code | 6, 31, 41, 63 | `math`, `service_tax`, `base_bill` (original), loop var `t` never used | Removed them |
| `== None` comparison + redundant if/else (E711, C0121, R1703, R1705) | Style | 32-37 | Non-idiomatic None check; if/else just returns a bool | `return order is not None and not order["is_settled"]` |
| Non-snake_case function names (C0103) | Style | 15, 23, 30, 40 | `placeTableOrder`, `voidTableOrder`, etc. violate PEP 8 | Renamed to `place_table_order`, `void_table_order`, `check_table_status`, `calculate_discounted_bill` |
| Missing docstrings (C0116) | Style | 15-61 | No function documents its purpose | Added one-line docstrings to all functions |
| Shadowed global `orders` (W0621) | Style | 61 | Parameter name hides module variable | Renamed parameter to `order_book`; used `sum()` generator |
| Line too long (E501, C0301) | Style | 18, 19, 75 | Lines over 79 chars | Wrapped dict literal across lines; f-string shortened |
| No final newline (W292, C0304) | Style | 83 | File does not end with `\n` | Added newline |
| `main()` runs on import | Design | 83 | Importing the module executes the demo | Added `if __name__ == "__main__":` guard |
| Magic number 15.0 | Maintainability | 18 | Dish price hardcoded | Extracted `PRICE_PER_DISH` constant |

## Results

| Tool | Before | After |
|---|---|---|
| Pylint | 4.81 / 10 (26 messages) | **10.00 / 10** |
| Bandit | 5 issues (2 High, 1 Medium, 2 Low) | **0 issues** |
| Flake8 | 9 issues | **0 issues** |

## Commits
1. Baseline reports (before)
2. Fix Bandit findings
3. Fix Pylint findings
4. Fix Flake8 findings
