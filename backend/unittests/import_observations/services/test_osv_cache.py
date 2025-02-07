from datetime import datetime
from json import loads
from unittest.mock import patch

from django.utils import timezone
from requests import Response
from requests.exceptions import HTTPError

from application.import_observations.models import OSV_Cache
from application.import_observations.services.osv_cache import get_osv_vulnerability
from unittests.base_test_case import BaseTestCase


class MockResponse:
    def __init__(self, osv_data):
        self.osv_data = osv_data

    def raise_for_status(self):
        pass

    def text(self):
        return self.osv_data


class TestImportObservations(BaseTestCase):
    def setUp(self):
        self.osv_id = "PYSEC-2024-157"
        self.osv_data = '{"id":"PYSEC-2024-157","details":"An issue was discovered in Django 5.1 before 5.1.4, 5.0 before 5.0.10, and 4.2 before 4.2.17. Direct usage of the django.db.models.fields.json.HasKey lookup, when an Oracle database is used, is subject to SQL injection if untrusted data is used as an lhs value. (Applications that use the jsonfield.has_key lookup via __ are unaffected.)","aliases":["CVE-2024-53908","GHSA-m9g8-fxxm-xg86"],"modified":"2025-01-14T05:56:57.527258Z","published":"2024-12-06T12:15:18Z","references":[{"type":"WEB","url":"https://docs.djangoproject.com/en/dev/releases/security/"},{"type":"WEB","url":"https://groups.google.com/g/django-announce"},{"type":"WEB","url":"https://www.openwall.com/lists/oss-security/2024/12/04/3"}],"affected":[{"package":{"name":"django","ecosystem":"PyPI","purl":"pkg:pypi/django"},"ranges":[{"type":"ECOSYSTEM","events":[{"introduced":"5.1"},{"fixed":"5.1.4"},{"introduced":"5.0"},{"fixed":"5.0.10"},{"introduced":"4.2"},{"fixed":"4.2.17"}]}],"versions":["4.2","4.2.1","4.2.10","4.2.11","4.2.12","4.2.13","4.2.14","4.2.15","4.2.16","4.2.2","4.2.3","4.2.4","4.2.5","4.2.6","4.2.7","4.2.8","4.2.9","5.0","5.0.1","5.0.2","5.0.3","5.0.4","5.0.5","5.0.6","5.0.7","5.0.8","5.0.9","5.1","5.1.1","5.1.2","5.1.3"],"database_specific":{"source":"https://github.com/pypa/advisory-database/blob/main/vulns/django/PYSEC-2024-157.yaml"}}],"schema_version":"1.6.0"}'
        self.osv_modified = datetime(
            2025, 1, 14, 5, 22, 11, 817473, timezone.get_current_timezone()
        )

    @patch("requests.get")
    def test_osv_cache_error(self, mock_requests_get):
        response = Response()
        response.status_code = 500
        response.reason = "unknown reason"
        response.url = "https://api.osv.dev/v1/vulns/CVE-2021-1234"
        mock_requests_get.return_value = response
        with self.assertRaises(HTTPError) as e:
            get_osv_vulnerability("CVE-2021-1234", timezone.now())

        self.assertEqual(
            "500 Server Error: unknown reason for url: https://api.osv.dev/v1/vulns/CVE-2021-1234",
            str(e.exception),
        )
        mock_requests_get.assert_called_once_with(
            url="https://api.osv.dev/v1/vulns/CVE-2021-1234",
            timeout=60,
        )

    @patch("requests.get")
    def test_osv_cache_from_database(self, mock_requests_get):
        OSV_Cache(
            osv_id=self.osv_id, modified=self.osv_modified, data=self.osv_data
        ).save()

        data = get_osv_vulnerability(self.osv_id, self.osv_modified)

        self.assertEqual(loads(self.osv_data), data)
        mock_requests_get.assert_not_called()

    @patch("requests.get")
    def test_osv_cache_not_in_database(self, mock_requests_get):
        response = MockResponse(self.osv_data)
        mock_requests_get.return_value = response

        data = get_osv_vulnerability(self.osv_id, self.osv_modified)

        self.assertEqual(loads(self.osv_data), data)
        mock_requests_get.assert_called_once_with(
            url="https://api.osv.dev/v1/vulns/PYSEC-2024-157",
            timeout=60,
        )
        osv_cache = OSV_Cache.objects.get(osv_id=self.osv_id)
        self.assertEqual(self.osv_data, osv_cache.data)
        self.assertEqual(self.osv_modified, osv_cache.modified)

    @patch("requests.get")
    def test_osv_cache_modified(self, mock_requests_get):
        OSV_Cache(
            osv_id=self.osv_id, modified=self.osv_modified, data=self.osv_data
        ).save()
        response = MockResponse(self.osv_data)
        mock_requests_get.return_value = response

        modified_now = timezone.now()

        data = get_osv_vulnerability(self.osv_id, modified_now)

        self.assertEqual(loads(self.osv_data), data)
        mock_requests_get.assert_called_once_with(
            url="https://api.osv.dev/v1/vulns/PYSEC-2024-157",
            timeout=60,
        )
        osv_cache = OSV_Cache.objects.get(osv_id=self.osv_id)
        self.assertEqual(self.osv_data, osv_cache.data)
        self.assertEqual(modified_now, osv_cache.modified)
