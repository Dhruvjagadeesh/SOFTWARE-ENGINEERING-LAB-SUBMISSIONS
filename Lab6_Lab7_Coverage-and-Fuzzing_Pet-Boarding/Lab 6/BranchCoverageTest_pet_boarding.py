"""Lab 6 - Branch coverage tests for pet_boarding.py

Goal: make every decision (if / elif / and-condition) evaluate to both True and
False (>= 90% branch coverage; this suite reaches 100%).

Run:
    coverage run --branch -m pytest BranchCoverageTest_pet_boarding.py
    coverage report -m
"""
import pytest
from pet_boarding import boarding_fee, admission_ok, checkout_status


# ---------------------------------------------------------------- boarding_fee
class TestBoardingFeeValidation:
    def test_unknown_pet_type_raises(self):
        with pytest.raises(ValueError, match="unknown pet type"):
            boarding_fee("hamster", 3, False)

    def test_known_pet_type_does_not_raise(self):
        assert boarding_fee("cat", 1, False) == 0

    def test_negative_days_raises(self):
        with pytest.raises(ValueError, match="invalid days"):
            boarding_fee("cat", -1, False)

    def test_zero_days_is_valid(self):
        assert boarding_fee("dog", 0, False) == 0


class TestBoardingFeeIncludedDays:
    def test_premium_non_rabbit_gets_extra_included_day(self):
        # cat: 3 + 1 premium = 4 included -> 4 days is free
        assert boarding_fee("cat", 4, True) == 0
        assert boarding_fee("cat", 5, True) == 20

    def test_non_premium_gets_no_bonus_day(self):
        # cat: 3 included -> 4 days = 1 extra day
        assert boarding_fee("cat", 4, False) == 20

    def test_premium_rabbit_gets_no_bonus_day(self):
        # rabbit: 4 included even when premium -> 5 days = 1 extra day
        assert boarding_fee("rabbit", 4, True) == 0
        assert boarding_fee("rabbit", 5, True) == 20

    def test_exactly_included_days_is_free(self):
        assert boarding_fee("dog", 2, False) == 0

    def test_fewer_than_included_days_is_free(self):
        assert boarding_fee("rabbit", 1, False) == 0


class TestBoardingFeeRates:
    def test_dog_rate_is_30(self):
        assert boarding_fee("dog", 5, False) == 3 * 30

    def test_cat_rate_is_20(self):
        assert boarding_fee("cat", 5, False) == 2 * 20

    def test_rabbit_rate_is_20(self):
        assert boarding_fee("rabbit", 6, False) == 2 * 20


class TestBoardingFeeLongStaySurcharge:
    def test_extra_exactly_10_has_no_surcharge(self):
        # dog: 2 included, 12 days -> extra = 10 -> not > 10
        assert boarding_fee("dog", 12, False) == 10 * 30

    def test_extra_11_dog_surcharge(self):
        # dog: 13 days -> extra = 11 -> rate 30 + 10 + 5 = 45
        assert boarding_fee("dog", 13, False) == 11 * 45

    def test_extra_11_cat_surcharge(self):
        # cat: 14 days -> extra = 11 -> rate 20 + 10 = 30 (no dog add-on)
        assert boarding_fee("cat", 14, False) == 11 * 30

    def test_extra_11_rabbit_surcharge(self):
        assert boarding_fee("rabbit", 15, False) == 11 * 30


# ---------------------------------------------------------------- admission_ok
class TestAdmissionOk:
    def test_senior_with_three_vaccinations(self):
        assert admission_ok(12, 3, True) is True

    def test_senior_with_two_vaccinations_rejected(self):
        assert admission_ok(12, 2, True) is False

    def test_senior_ignores_age_rule(self):
        # senior path returns before the age check
        assert admission_ok(0, 3, True) is True

    def test_non_senior_under_one_year_rejected(self):
        assert admission_ok(0.5, 5, False) is False

    def test_non_senior_exactly_one_year_with_two_vaccinations(self):
        assert admission_ok(1, 2, False) is True

    def test_non_senior_with_one_vaccination_rejected(self):
        assert admission_ok(4, 1, False) is False

    def test_admission_ok_example(self):
        assert admission_ok(4, 2, False) is True


# ------------------------------------------------------------- checkout_status
class TestCheckoutStatus:
    # cutoff table:
    #   short weekday = 15, long weekday = 30, short weekend = 35, long weekend = 50
    @pytest.mark.parametrize(
        "long_stay, weekend, cutoff",
        [(False, False, 15), (True, False, 30), (False, True, 35), (True, True, 50)],
    )
    def test_open_at_cutoff(self, long_stay, weekend, cutoff):
        assert checkout_status(cutoff, long_stay, weekend) == "open"

    @pytest.mark.parametrize(
        "long_stay, weekend, cutoff",
        [(False, False, 15), (True, False, 30), (False, True, 35), (True, True, 50)],
    )
    def test_late_just_below_cutoff(self, long_stay, weekend, cutoff):
        assert checkout_status(cutoff - 1, long_stay, weekend) == "late"

    @pytest.mark.parametrize(
        "long_stay, weekend, cutoff",
        [(False, False, 15), (True, False, 30), (False, True, 35), (True, True, 50)],
    )
    def test_late_lower_boundary(self, long_stay, weekend, cutoff):
        assert checkout_status(cutoff - 15, long_stay, weekend) == "late"

    @pytest.mark.parametrize(
        "long_stay, weekend, cutoff",
        [(False, False, 15), (True, False, 30), (False, True, 35), (True, True, 50)],
    )
    def test_closed_below_late_window(self, long_stay, weekend, cutoff):
        assert checkout_status(cutoff - 16, long_stay, weekend) == "closed"
