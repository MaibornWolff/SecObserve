from typing import Optional


class Age_Choices:
    AGE_DAY = "Today"
    AGE_WEEK = "Past 7 days"
    AGE_MONTH = "Past 30 days"
    AGE_QUARTER = "Past 90 days"
    AGE_YEAR = "Past 365 days"

    AGE_CHOICES = [
        (AGE_DAY, AGE_DAY),
        (AGE_WEEK, AGE_WEEK),
        (AGE_MONTH, AGE_MONTH),
        (AGE_QUARTER, AGE_QUARTER),
        (AGE_YEAR, AGE_YEAR),
    ]

    @classmethod
    def get_days_from_age(cls, value: "Age_Choices") -> Optional[int]:
        if value == cls.AGE_DAY:
            days = 0
        elif value == cls.AGE_WEEK:
            days = 7
        elif value == cls.AGE_MONTH:
            days = 30
        elif value == cls.AGE_QUARTER:
            days = 90
        elif value == cls.AGE_YEAR:
            days = 365
        else:
            days = None
        return days


class VEX_Justification_Styles:
    STYLE_CSAF_OPENVEX = "CSAF/OpenVEX"
    STYLE_CYCLONEDX = "CycloneDX"

    STYLE_CHOICES = [
        (STYLE_CSAF_OPENVEX, STYLE_CSAF_OPENVEX),
        (STYLE_CYCLONEDX, STYLE_CYCLONEDX),
    ]
