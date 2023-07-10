from typing import Optional

AGE_WEEK = "Past 7 days"
AGE_MONTH = "Past 30 days"
AGE_QUARTER = "Past 90 days"
AGE_YEAR = "Past 365 days"

AGE_CHOICES = [
    (AGE_WEEK, AGE_WEEK),
    (AGE_MONTH, AGE_MONTH),
    (AGE_QUARTER, AGE_QUARTER),
    (AGE_YEAR, AGE_YEAR),
]


def get_days(age: str) -> Optional[int]:
    if age == AGE_WEEK:
        days = 7
    elif age == AGE_MONTH:
        days = 30
    elif age == AGE_QUARTER:
        days = 90
    elif age == AGE_YEAR:
        days = 365
    else:
        days = None

    return days
