from unittest import TestCase

from application.import_observations.types import ExtendedSemVer
from application.import_observations.rpm import RpmVersion


class TestExtendedSemVer(TestCase):
    def test_parse(self):
        ext_semver = ExtendedSemVer.parse("1.2.3-alpha")
        self.assertEqual(ext_semver.prefix, None)
        self.assertEqual(ext_semver.semver, "1.2.3-alpha")

        ext_semver = ExtendedSemVer.parse("v1.2.3-alpha")
        self.assertEqual(ext_semver.prefix, None)
        self.assertEqual(ext_semver.semver, "1.2.3-alpha")

        ext_semver = ExtendedSemVer.parse("0")
        self.assertEqual(ext_semver.prefix, None)
        self.assertEqual(ext_semver.semver, "0.0.0")

        ext_semver = ExtendedSemVer.parse("1.2")
        self.assertEqual(ext_semver.prefix, None)
        ext_semver = ExtendedSemVer.parse("1.2.0")

        ext_semver = ExtendedSemVer.parse("1:1.2.3")
        self.assertEqual(ext_semver.prefix, 1)
        self.assertEqual(ext_semver.semver, "1.2.3")

        ext_semver = ExtendedSemVer.parse("1:1.2-alpha")
        self.assertEqual(ext_semver.prefix, 1)
        self.assertEqual(ext_semver.semver, "1.2.0-alpha")

        ext_semver = ExtendedSemVer.parse(None)
        self.assertEqual(ext_semver, None)

        ext_semver = ExtendedSemVer.parse("test")
        self.assertEqual(ext_semver, None)

        ext_semver = ExtendedSemVer.parse("a:1.2")
        self.assertEqual(ext_semver, None)

        rpm_ver = RpmVersion.from_string("1:21.0.6.0.7-1.el9")
        self.assertEqual(rpm_ver.epoch, 1)
        self.assertEqual(rpm_ver.version, "21.0.6.0.7")
        self.assertEqual(rpm_ver.release, "1.el9")

    def test_eq(self):
        ext_semver1 = ExtendedSemVer.parse("1.2.3-alpha")
        self.assertNotEqual(ext_semver1, None)
        self.assertNotEqual(None, ext_semver1)

        ext_semver1 = ExtendedSemVer.parse("1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1.2.3-alpha")
        self.assertEqual(ext_semver1, ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1.2.3-beta")
        self.assertNotEqual(ext_semver1, ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1:1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1:1.2.3-alpha")
        self.assertEqual(ext_semver1, ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1:1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("2:1.2.3-alpha")
        self.assertNotEqual(ext_semver1, ext_semver2)

    def test_gt(self):
        ext_semver1 = ExtendedSemVer.parse("1.2.3-alpha")
        self.assertFalse(ext_semver1 > None)
        self.assertFalse(None > ext_semver1)

        ext_semver1 = ExtendedSemVer.parse("1:1.2.3-beta")
        ext_semver2 = ExtendedSemVer.parse("1.2.3-alpha")
        self.assertFalse(ext_semver1 > ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1.2.3-beta")
        ext_semver2 = ExtendedSemVer.parse("1:1.2.3-alpha")
        self.assertFalse(ext_semver1 > ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1.2.3-alpha")
        self.assertFalse(ext_semver1 > ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1.2.3-beta")
        self.assertFalse(ext_semver1 > ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1.2.3-beta")
        ext_semver2 = ExtendedSemVer.parse("1.2.3-alpha")
        self.assertTrue(ext_semver1 > ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1:1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1:1.2.3-alpha")
        self.assertFalse(ext_semver1 > ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1:1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("2:1.2.3-alpha")
        self.assertFalse(ext_semver1 > ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("2:1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1:1.2.3-alpha")
        self.assertTrue(ext_semver1 > ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1:1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1:1.2.3-beta")
        self.assertFalse(ext_semver1 > ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1:1.2.3-beta")
        ext_semver2 = ExtendedSemVer.parse("1:1.2.3-alpha")
        self.assertTrue(ext_semver1 > ext_semver2)

        rpm_ver1 = RpmVersion.from_string("1:21.0.6.0.7-1.el9")
        rpm_ver2 = RpmVersion.from_string("1:21.0.1.0.12-2.el9")
        self.assertTrue(rpm_ver1 > rpm_ver2)

    def test_ge(self):
        ext_semver1 = ExtendedSemVer.parse("1.2.3-alpha")
        self.assertFalse(ext_semver1 >= None)
        self.assertFalse(None >= ext_semver1)

        ext_semver1 = ExtendedSemVer.parse("1:1.2.3-beta")
        ext_semver2 = ExtendedSemVer.parse("1.2.3-alpha")
        self.assertFalse(ext_semver1 >= ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1.2.3-beta")
        ext_semver2 = ExtendedSemVer.parse("1:1.2.3-alpha")
        self.assertFalse(ext_semver1 >= ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1.2.3-alpha")
        self.assertTrue(ext_semver1 >= ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1.2.3-beta")
        self.assertFalse(ext_semver1 >= ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1.2.3-beta")
        ext_semver2 = ExtendedSemVer.parse("1.2.3-alpha")
        self.assertTrue(ext_semver1 >= ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1:1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1:1.2.3-alpha")
        self.assertTrue(ext_semver1 >= ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1:1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("2:1.2.3-alpha")
        self.assertFalse(ext_semver1 >= ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("2:1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1:1.2.3-alpha")
        self.assertTrue(ext_semver1 >= ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1:1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1:1.2.3-beta")
        self.assertFalse(ext_semver1 >= ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1:1.2.3-beta")
        ext_semver2 = ExtendedSemVer.parse("1:1.2.3-alpha")
        self.assertTrue(ext_semver1 >= ext_semver2)

    def test_lt(self):
        ext_semver1 = ExtendedSemVer.parse("1.2.3-alpha")
        self.assertFalse(ext_semver1 < None)
        self.assertFalse(None < ext_semver1)

        ext_semver1 = ExtendedSemVer.parse("1:1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1.2.3-beta")
        self.assertFalse(ext_semver1 < ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1:1.2.3-beta")
        self.assertFalse(ext_semver1 < ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1.2.3-alpha")
        self.assertFalse(ext_semver1 < ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1.2.3-beta")
        self.assertTrue(ext_semver1 < ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1.2.3-beta")
        ext_semver2 = ExtendedSemVer.parse("1.2.3-alpha")
        self.assertFalse(ext_semver1 < ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1:1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1:1.2.3-alpha")
        self.assertFalse(ext_semver1 < ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1:1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("2:1.2.3-alpha")
        self.assertTrue(ext_semver1 < ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("2:1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1:1.2.3-alpha")
        self.assertFalse(ext_semver1 < ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1:1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1:1.2.3-beta")
        self.assertTrue(ext_semver1 < ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1:1.2.3-beta")
        ext_semver2 = ExtendedSemVer.parse("1:1.2.3-alpha")
        self.assertFalse(ext_semver1 < ext_semver2)

    def test_le(self):
        ext_semver1 = ExtendedSemVer.parse("1.2.3-alpha")
        self.assertFalse(ext_semver1 <= None)
        self.assertFalse(None <= ext_semver1)

        ext_semver1 = ExtendedSemVer.parse("1:1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1.2.3-beta")
        self.assertFalse(ext_semver1 <= ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1:1.2.3-beta")
        self.assertFalse(ext_semver1 <= ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1.2.3-alpha")
        self.assertTrue(ext_semver1 <= ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1.2.3-beta")
        self.assertTrue(ext_semver1 <= ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1.2.3-beta")
        ext_semver2 = ExtendedSemVer.parse("1.2.3-alpha")
        self.assertFalse(ext_semver1 <= ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1:1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1:1.2.3-alpha")
        self.assertTrue(ext_semver1 <= ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1:1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("2:1.2.3-alpha")
        self.assertTrue(ext_semver1 <= ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("2:1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1:1.2.3-alpha")
        self.assertFalse(ext_semver1 <= ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1:1.2.3-alpha")
        ext_semver2 = ExtendedSemVer.parse("1:1.2.3-beta")
        self.assertTrue(ext_semver1 <= ext_semver2)

        ext_semver1 = ExtendedSemVer.parse("1:1.2.3-beta")
        ext_semver2 = ExtendedSemVer.parse("1:1.2.3-alpha")
        self.assertFalse(ext_semver1 <= ext_semver2)
