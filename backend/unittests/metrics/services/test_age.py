from application.metrics.services.age import (
    AGE_MONTH,
    AGE_QUARTER,
    AGE_WEEK,
    AGE_YEAR,
    get_days,
)
from unittests.base_test_case import BaseTestCase


class TestAge(BaseTestCase):
    def test_get_age(self):
        self.assertEqual(get_days(AGE_WEEK), 7)
        self.assertEqual(get_days(AGE_MONTH), 30)
        self.assertEqual(get_days(AGE_QUARTER), 90)
        self.assertEqual(get_days(AGE_YEAR), 365)
        self.assertEqual(get_days("Past 3650 days"), None)
