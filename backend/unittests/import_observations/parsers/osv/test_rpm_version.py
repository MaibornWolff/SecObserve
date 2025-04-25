from application.import_observations.parsers.osv.rpm import RpmVersion
from unittests.base_test_case import BaseTestCase


class TestRpmVersion(BaseTestCase):
    def test_parse_version(self):
        rpm_ver = RpmVersion.from_string("1:21.0.6.0.7-1.el9")
        self.assertEqual(rpm_ver.epoch, 1)
        self.assertEqual(rpm_ver.version, "21.0.6.0.7")
        self.assertEqual(rpm_ver.release, "1.el9")

    def test_comparisons(self):
        rpm_ver1 = RpmVersion.from_string("1:21.0.6.0.7-1.el9")
        rpm_ver2 = RpmVersion.from_string("1:21.0.1.0.12-2.el9")
        self.assertTrue(rpm_ver1 > rpm_ver2)
        self.assertTrue(rpm_ver2 < rpm_ver1)
        self.assertFalse(rpm_ver1 == rpm_ver2)
