"""Lab 7 - Fuzz tests (Hypothesis) for pet_boarding.py

Three layers per function:
  1. *_no_crash          - the handout's property: ANY input (text, None) must not raise.
  2. *_structured        - grammar-aware fuzzing: strings built from the characters the
                           parser cares about (digits, separators, signs, 'nan', 'inf', ...)
                           so Hypothesis reaches deep into the parsing code.
  3. *_result_is_sane    - whenever a function accepts an input, its output must satisfy
                           the business invariants (finite, non-negative, right type).
Plus explicit regression tests for the bugs fuzzing discovered.

Run:  python -m pytest test_pet_boarding.py
"""
import math

import pytest
from hypothesis import given, settings, strategies as st

from pet_boarding import parse_booking, stay_average, payable_fee

# Anything a user (or an attacker) could hand to a text parser.
anything = st.one_of(
    st.text(),
    st.none(),
    st.integers(),
    st.floats(allow_nan=True, allow_infinity=True),
    st.binary(),
    st.lists(st.integers(), max_size=4),
)

# Characters that exercise the parsing rules: separators, signs, exponents, specials.
BOOKING_ALPHABET = "dogcat 0123456789.:-+eE_infatyNI\t"
CSV_ALPHABET = "0123456789,.- +_ \t"
FEE_ALPHABET = "0123456789.|-+eE_infatyNI \t"


# ============================================================== parse_booking
@given(st.text() | st.none())
def test_parse_booking_no_crash(s):
    try:
        parse_booking(s)
    except Exception as e:  # noqa: BLE001 - the whole point is to catch anything
        assert False, f"parse_booking crashed with: {e!r}"


@given(anything)
def test_parse_booking_any_type_no_crash(s):
    try:
        parse_booking(s)
    except Exception as e:  # noqa: BLE001
        assert False, f"parse_booking crashed with: {e!r}"


@given(st.text(alphabet=BOOKING_ALPHABET))
def test_parse_booking_structured_no_crash(s):
    try:
        parse_booking(s)
    except Exception as e:  # noqa: BLE001
        assert False, f"parse_booking({s!r}) crashed with: {e!r}"


@given(st.text(alphabet=BOOKING_ALPHABET) | st.text())
def test_parse_booking_result_is_sane(s):
    result = parse_booking(s)
    if result is not None:
        pet, days = result
        assert isinstance(pet, str) and pet.strip() != ""
        assert isinstance(days, float) and math.isfinite(days) and days >= 0


@given(
    st.text(alphabet=st.characters(whitelist_categories=("Lu", "Ll")), min_size=1),
    st.integers(min_value=0, max_value=10_000),
)
def test_parse_booking_valid_roundtrip(pet, days):
    assert parse_booking(f"{pet}:{days}") == (pet.strip().title(), float(days))


@pytest.mark.parametrize(
    "bad",
    [
        None, "", "dog", "dog:", ":5", " : ", "dog:5:6", "dog:abc",
        "dog:nan", "dog:inf", "dog:-inf", "dog:-1", "dog:1e999", "dog:1_0",
        5, 5.5, b"dog:5", ["dog:5"],
    ],
)
def test_parse_booking_rejects_bad_input(bad):
    assert parse_booking(bad) is None


@pytest.mark.parametrize(
    "text, expected",
    [("dog:5", ("Dog", 5.0)), ("  cAT : 2.5 ", ("Cat", 2.5)), ("rabbit:0", ("Rabbit", 0.0))],
)
def test_parse_booking_valid_examples(text, expected):
    assert parse_booking(text) == expected


# ============================================================== stay_average
@given(st.text() | st.none())
def test_stay_average_no_crash(s):
    try:
        stay_average(s)
    except Exception as e:  # noqa: BLE001
        assert False, f"stay_average crashed with: {e!r}"


@given(anything)
def test_stay_average_any_type_no_crash(s):
    try:
        stay_average(s)
    except Exception as e:  # noqa: BLE001
        assert False, f"stay_average crashed with: {e!r}"


@given(st.text(alphabet=CSV_ALPHABET))
def test_stay_average_structured_no_crash(s):
    try:
        stay_average(s)
    except Exception as e:  # noqa: BLE001
        assert False, f"stay_average({s!r}) crashed with: {e!r}"


@given(st.text(alphabet=CSV_ALPHABET) | st.text())
def test_stay_average_result_is_sane(s):
    result = stay_average(s)
    if result is not None:
        assert isinstance(result, int) and result >= 0


@given(st.lists(st.integers(min_value=0, max_value=365), min_size=1, max_size=50))
def test_stay_average_valid_is_between_min_and_max(values):
    result = stay_average(",".join(map(str, values)))
    assert min(values) <= result <= max(values)


@pytest.mark.parametrize(
    "bad",
    [None, "", " ", ",", "1,,3", "1,2,", ",1", "one,two", "1.5,2", "-1,2", "1,-2",
     "1_0,2", "1;2", 7, ["1", "2"]],
)
def test_stay_average_rejects_bad_input(bad):
    assert stay_average(bad) is None


@pytest.mark.parametrize(
    "text, expected", [("2,5,7", 4), ("3", 3), (" 2 , 4 ", 3), ("0,0", 0)]
)
def test_stay_average_valid_examples(text, expected):
    assert stay_average(text) == expected


# ============================================================== payable_fee
@given(st.text() | st.none())
def test_payable_fee_no_crash(s):
    try:
        payable_fee(s)
    except Exception as e:  # noqa: BLE001
        assert False, f"payable_fee crashed with: {e!r}"


@given(anything)
def test_payable_fee_any_type_no_crash(s):
    try:
        payable_fee(s)
    except Exception as e:  # noqa: BLE001
        assert False, f"payable_fee crashed with: {e!r}"


@given(st.text(alphabet=FEE_ALPHABET))
def test_payable_fee_structured_no_crash(s):
    try:
        payable_fee(s)
    except Exception as e:  # noqa: BLE001
        assert False, f"payable_fee({s!r}) crashed with: {e!r}"


@given(st.text(alphabet=FEE_ALPHABET) | st.text())
def test_payable_fee_result_is_sane(s):
    result = payable_fee(s)
    if result is not None:
        assert isinstance(result, float) and math.isfinite(result) and result >= 0


@given(
    st.floats(min_value=0, max_value=1e9, allow_nan=False),
    st.floats(min_value=0, max_value=1e9, allow_nan=False),
)
def test_payable_fee_valid_matches_formula(fee, discount):
    result = payable_fee(f"{fee!r}|{discount!r}")
    assert result == pytest.approx(max(fee * 1.18 - discount, 0), rel=1e-9, abs=1e-9)


@pytest.mark.parametrize(
    "bad",
    [None, "", "100", "|", "100|", "|5", "1|2|3", "abc|1", "1|abc", "nan|0", "0|nan",
     "inf|0", "1e999|0", "-100|0", "100|-5", "1_0|1", 5, ["1|2"]],
)
def test_payable_fee_rejects_bad_input(bad):
    assert payable_fee(bad) is None


@pytest.mark.parametrize(
    "text, expected",
    [("1500|100", 1670.0), ("100|0", 118.0), ("10|1000", 0.0), (" 200 | 20 ", 216.0)],
)
def test_payable_fee_valid_examples(text, expected):
    assert payable_fee(text) == pytest.approx(expected)
