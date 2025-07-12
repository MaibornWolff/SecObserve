from datetime import timedelta

from django.utils import timezone

from unittests.authorization.api.test_authorization import (
    APITest,
    TestAuthorizationBase,
)


class TestAuthorizationProductMetrics(TestAuthorizationBase):
    def test_authorization_metrics(self):
        yesterday = (timezone.now() - timedelta(days=1)).date().isoformat()
        today = timezone.now().date().isoformat()

        expected_data = "{'open_critical': 7, 'open_high': 9, 'open_medium': 11, 'open_low': 13, 'open_none': 15, 'open_unknown': 17, 'open': 19, 'resolved': 21, 'duplicate': 23, 'false_positive': 25, 'in_review': 27, 'not_affected': 29, 'not_security': 31, 'risk_accepted': 33}"
        self._test_api(
            APITest(
                "db_admin",
                "get",
                "/api/metrics/product_metrics_current/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'2023-07-09': {'open_critical': 5, 'open_high': 7, 'open_medium': 9, 'open_low': 11, 'open_none': 13, 'open_unknown': 15, 'open': 17, 'resolved': 19, 'duplicate': 21, 'false_positive': 23, 'in_review': 25, 'not_affected': 27, 'not_security': 29, 'risk_accepted': 31}, '2023-07-10': {'open_critical': 7, 'open_high': 9, 'open_medium': 11, 'open_low': 13, 'open_none': 15, 'open_unknown': 17, 'open': 19, 'resolved': 21, 'duplicate': 23, 'false_positive': 25, 'in_review': 27, 'not_affected': 29, 'not_security': 31, 'risk_accepted': 33}}"
        expected_data = expected_data.replace("2023-07-10", today)
        expected_data = expected_data.replace("2023-07-09", yesterday)
        self._test_api(
            APITest(
                "db_admin",
                "get",
                "/api/metrics/product_metrics_timeline/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'open_critical': 2, 'open_high': 3, 'open_medium': 4, 'open_low': 5, 'open_none': 6, 'open_unknown': 7, 'open': 8, 'resolved': 9, 'duplicate': 10, 'false_positive': 11, 'in_review': 12, 'not_affected': 13, 'not_security': 14, 'risk_accepted': 15}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/metrics/product_metrics_current/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'2023-07-09': {'open_critical': 1, 'open_high': 2, 'open_medium': 3, 'open_low': 4, 'open_none': 5, 'open_unknown': 6, 'open': 7, 'resolved': 8, 'duplicate': 9, 'false_positive': 10, 'in_review': 11, 'not_affected': 12, 'not_security': 13, 'risk_accepted': 14}, '2023-07-10': {'open_critical': 2, 'open_high': 3, 'open_medium': 4, 'open_low': 5, 'open_none': 6, 'open_unknown': 7, 'open': 8, 'resolved': 9, 'duplicate': 10, 'false_positive': 11, 'in_review': 12, 'not_affected': 13, 'not_security': 14, 'risk_accepted': 15}}"
        expected_data = expected_data.replace("2023-07-10", today)
        expected_data = expected_data.replace("2023-07-09", yesterday)
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/metrics/product_metrics_timeline/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'open_critical': 2, 'open_high': 3, 'open_medium': 4, 'open_low': 5, 'open_none': 6, 'open_unknown': 7, 'open': 8, 'resolved': 9, 'duplicate': 10, 'false_positive': 11, 'in_review': 12, 'not_affected': 13, 'not_security': 14, 'risk_accepted': 15}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/metrics/product_metrics_current/?product_id=1",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'2023-07-09': {'open_critical': 1, 'open_high': 2, 'open_medium': 3, 'open_low': 4, 'open_none': 5, 'open_unknown': 6, 'open': 7, 'resolved': 8, 'duplicate': 9, 'false_positive': 10, 'in_review': 11, 'not_affected': 12, 'not_security': 13, 'risk_accepted': 14}, '2023-07-10': {'open_critical': 2, 'open_high': 3, 'open_medium': 4, 'open_low': 5, 'open_none': 6, 'open_unknown': 7, 'open': 8, 'resolved': 9, 'duplicate': 10, 'false_positive': 11, 'in_review': 12, 'not_affected': 13, 'not_security': 14, 'risk_accepted': 15}}"
        expected_data = expected_data.replace("2023-07-10", today)
        expected_data = expected_data.replace("2023-07-09", yesterday)
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/metrics/product_metrics_timeline/?product_id=1",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'message': 'You do not have permission to perform this action.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/metrics/product_metrics_current/?product_id=2",
                None,
                403,
                expected_data,
            )
        )
        expected_data = "{'message': 'You do not have permission to perform this action.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/metrics/product_metrics_timeline/?product_id=2",
                None,
                403,
                expected_data,
            )
        )
