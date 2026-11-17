"""Pet boarding input parsing - hardened against malformed input (Lab 7).

Design rule: every public function validates its input and returns ``None``
when the input is invalid, instead of raising.  Callers (see ``main``) check
for ``None`` and show a friendly message.
"""
import math

TAX_RATE = 1.18


def _to_finite_non_negative_float(token):
    """Parse ``token`` as a finite float >= 0, or return None."""
    if not isinstance(token, str) or "_" in token:   # "1_0" is legal Python, not legal input
        return None
    try:
        value = float(token)
    except ValueError:
        return None
    if not math.isfinite(value) or value < 0:        # rejects nan, inf, 1e999, negatives
        return None
    return value


def _to_non_negative_int(token):
    """Parse ``token`` as a whole number >= 0, or return None."""
    if not isinstance(token, str) or "_" in token:
        return None
    try:
        value = int(token)
    except ValueError:
        return None
    return value if value >= 0 else None


def parse_booking(text):
    """'dog:5' -> ('Dog', 5.0).  Returns None for invalid input."""
    if not isinstance(text, str):
        return None
    parts = text.split(":")
    if len(parts) != 2:                              # missing or extra ':'
        return None
    pet = parts[0].strip()
    days = _to_finite_non_negative_float(parts[1])
    if not pet or days is None:                      # empty name / bad days
        return None
    return pet.title(), days


def stay_average(days_csv):
    """'2,5,7' -> 4 (integer average).  Returns None for invalid input."""
    if not isinstance(days_csv, str):
        return None
    values = [_to_non_negative_int(item) for item in days_csv.split(",")]
    if not values or any(v is None for v in values):  # '', '1,,3', 'a,b', '-1,2' ...
        return None
    return sum(values) // len(values)


def payable_fee(text):
    """'1500|100' -> fee * 1.18 - discount, never below 0.  None for invalid input."""
    if not isinstance(text, str):
        return None
    parts = text.split("|")
    if len(parts) != 2:                              # missing or extra '|'
        return None
    fee = _to_finite_non_negative_float(parts[0])
    discount = _to_finite_non_negative_float(parts[1])
    if fee is None or discount is None:
        return None
    total = fee * TAX_RATE - discount
    if not math.isfinite(total):                     # fee * 1.18 can overflow to inf
        return None
    return max(total, 0.0)


def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter pet:days (e.g. dog:5): ")
    result = parse_booking(user_input)
    print("Pet and Days:", result if result is not None else "Invalid input (expected pet:days, days >= 0)")

    print("\n==== Running stay_average ====")
    user_input = input("Enter stay lengths in days as CSV (e.g. 2,5,7): ")
    result = stay_average(user_input)
    print("Average Stay:", result if result is not None else "Invalid input (expected whole numbers >= 0, comma separated)")

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 1500|100): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result if result is not None else "Invalid input (expected fee|discount, both >= 0)")


if __name__ == "__main__":
    main()
