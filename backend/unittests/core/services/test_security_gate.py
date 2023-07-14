from unittest.mock import patch

from constance.test import override_config

from application.core.models import Product
from application.core.services.security_gate import check_security_gate
from unittests.base_test_case import BaseTestCase


class TestSecurityGate(BaseTestCase):
    @patch("application.core.models.Product.save")
    @patch(
        "application.core.services.security_gate.send_product_security_gate_notification"
    )
    def test_check_security_gate_unchanged(self, notification_mock, save_mock):
        product = Product(security_gate_passed=None, security_gate_active=False)
        check_security_gate(product)
        self.assertIsNone(product.security_gate_passed)
        save_mock.assert_not_called()
        notification_mock.assert_not_called()

    @patch("application.core.models.Product.save")
    @patch(
        "application.core.services.security_gate.send_product_security_gate_notification"
    )
    def test_check_security_gate_false_and_changed(self, notification_mock, save_mock):
        product = Product(security_gate_passed=True, security_gate_active=False)
        check_security_gate(product)
        self.assertIsNone(product.security_gate_passed)
        save_mock.assert_called()
        notification_mock.assert_called_with(product)

    @patch("application.core.models.Observation.objects.filter")
    def test_check_security_gate_true_critical(self, mock):
        mock.return_value.count.return_value = 2
        product = Product(
            security_gate_passed=False,
            security_gate_active=True,
            security_gate_threshold_critical=1,
        )
        check_security_gate(product)
        self.assertFalse(product.security_gate_passed)

    @patch("application.core.models.Observation.objects.filter")
    def test_check_security_gate_true_high(self, mock):
        mock.return_value.count.return_value = 2
        product = Product(
            security_gate_passed=False,
            security_gate_active=True,
            security_gate_threshold_critical=3,
            security_gate_threshold_high=1,
        )
        check_security_gate(product)
        self.assertFalse(product.security_gate_passed)

    @patch("application.core.models.Observation.objects.filter")
    def test_check_security_gate_true_medium(self, mock):
        mock.return_value.count.return_value = 2
        product = Product(
            security_gate_passed=False,
            security_gate_active=True,
            security_gate_threshold_critical=3,
            security_gate_threshold_high=3,
            security_gate_threshold_medium=1,
        )
        check_security_gate(product)
        self.assertFalse(product.security_gate_passed)

    @patch("application.core.models.Observation.objects.filter")
    def test_check_security_gate_true_low(self, mock):
        mock.return_value.count.return_value = 2
        product = Product(
            security_gate_passed=False,
            security_gate_active=True,
            security_gate_threshold_critical=3,
            security_gate_threshold_high=3,
            security_gate_threshold_medium=3,
            security_gate_threshold_low=1,
        )
        check_security_gate(product)
        self.assertFalse(product.security_gate_passed)

    @patch("application.core.models.Observation.objects.filter")
    def test_check_security_gate_true_none(self, mock):
        mock.return_value.count.return_value = 2
        product = Product(
            security_gate_passed=False,
            security_gate_active=True,
            security_gate_threshold_critical=3,
            security_gate_threshold_high=3,
            security_gate_threshold_medium=3,
            security_gate_threshold_low=3,
            security_gate_threshold_none=1,
        )
        check_security_gate(product)
        self.assertFalse(product.security_gate_passed)

    @patch("application.core.models.Observation.objects.filter")
    def test_check_security_gate_true_unkown(self, mock):
        mock.return_value.count.return_value = 2
        product = Product(
            security_gate_passed=False,
            security_gate_active=True,
            security_gate_threshold_critical=3,
            security_gate_threshold_high=3,
            security_gate_threshold_medium=3,
            security_gate_threshold_low=3,
            security_gate_threshold_none=3,
            security_gate_threshold_unkown=1,
        )
        check_security_gate(product)
        self.assertFalse(product.security_gate_passed)

    @patch("application.core.models.Observation.objects.filter")
    def test_check_security_gate_true_no_match(self, mock):
        mock.return_value.count.return_value = 2
        product = Product(
            security_gate_passed=True,
            security_gate_active=True,
            security_gate_threshold_critical=3,
            security_gate_threshold_high=3,
            security_gate_threshold_medium=3,
            security_gate_threshold_low=3,
            security_gate_threshold_none=3,
            security_gate_threshold_unkown=3,
        )
        check_security_gate(product)
        self.assertTrue(product.security_gate_passed)

    @override_config(SECURITY_GATE_THRESHOLD_CRITICAL=1)
    @patch("application.core.models.Observation.objects.filter")
    def test_check_security_gate_none_critical(self, mock):
        mock.return_value.count.return_value = 2
        product = Product(
            security_gate_passed=False,
        )
        check_security_gate(product)
        self.assertFalse(product.security_gate_passed)

    @override_config(SECURITY_GATE_THRESHOLD_CRITICAL=3)
    @override_config(SECURITY_GATE_THRESHOLD_HIGH=1)
    @patch("application.core.models.Observation.objects.filter")
    def test_check_security_gate_none_high(self, mock):
        mock.return_value.count.return_value = 2
        product = Product(
            security_gate_passed=False,
        )
        check_security_gate(product)
        self.assertFalse(product.security_gate_passed)

    @override_config(SECURITY_GATE_THRESHOLD_CRITICAL=3)
    @override_config(SECURITY_GATE_THRESHOLD_HIGH=3)
    @override_config(SECURITY_GATE_THRESHOLD_MEDIUM=1)
    @patch("application.core.models.Observation.objects.filter")
    def test_check_security_gate_none_medium(self, mock):
        mock.return_value.count.return_value = 2
        product = Product(
            security_gate_passed=False,
        )
        check_security_gate(product)
        self.assertFalse(product.security_gate_passed)

    @override_config(SECURITY_GATE_THRESHOLD_CRITICAL=3)
    @override_config(SECURITY_GATE_THRESHOLD_HIGH=3)
    @override_config(SECURITY_GATE_THRESHOLD_MEDIUM=3)
    @override_config(SECURITY_GATE_THRESHOLD_LOW=1)
    @patch("application.core.models.Observation.objects.filter")
    def test_check_security_gate_none_low(self, mock):
        mock.return_value.count.return_value = 2
        product = Product(
            security_gate_passed=False,
        )
        check_security_gate(product)
        self.assertFalse(product.security_gate_passed)

    @override_config(SECURITY_GATE_THRESHOLD_CRITICAL=3)
    @override_config(SECURITY_GATE_THRESHOLD_HIGH=3)
    @override_config(SECURITY_GATE_THRESHOLD_MEDIUM=3)
    @override_config(SECURITY_GATE_THRESHOLD_LOW=3)
    @override_config(SECURITY_GATE_THRESHOLD_NONE=1)
    @patch("application.core.models.Observation.objects.filter")
    def test_check_security_gate_none_none(self, mock):
        mock.return_value.count.return_value = 2
        product = Product(
            security_gate_passed=False,
        )
        check_security_gate(product)
        self.assertFalse(product.security_gate_passed)

    @override_config(SECURITY_GATE_THRESHOLD_CRITICAL=3)
    @override_config(SECURITY_GATE_THRESHOLD_HIGH=3)
    @override_config(SECURITY_GATE_THRESHOLD_MEDIUM=3)
    @override_config(SECURITY_GATE_THRESHOLD_LOW=3)
    @override_config(SECURITY_GATE_THRESHOLD_NONE=3)
    @override_config(SECURITY_GATE_THRESHOLD_UNKOWN=1)
    @patch("application.core.models.Observation.objects.filter")
    def test_check_security_gate_none_unkown(self, mock):
        mock.return_value.count.return_value = 2
        product = Product(
            security_gate_passed=False,
        )
        check_security_gate(product)
        self.assertFalse(product.security_gate_passed)

    @override_config(SECURITY_GATE_THRESHOLD_CRITICAL=3)
    @override_config(SECURITY_GATE_THRESHOLD_HIGH=3)
    @override_config(SECURITY_GATE_THRESHOLD_MEDIUM=3)
    @override_config(SECURITY_GATE_THRESHOLD_LOW=3)
    @override_config(SECURITY_GATE_THRESHOLD_NONE=3)
    @override_config(SECURITY_GATE_THRESHOLD_UNKOWN=3)
    @patch("application.core.models.Observation.objects.filter")
    def test_check_security_gate_none_no_match(self, mock):
        mock.return_value.count.return_value = 2
        product = Product(
            security_gate_passed=True,
        )
        check_security_gate(product)
        self.assertTrue(product.security_gate_passed)

    @patch("application.core.models.Product.save")
    @patch(
        "application.core.services.security_gate.send_product_security_gate_notification"
    )
    @override_config(SECURITY_GATE_ACTIVE=False)
    def test_check_security_gate_general_false(self, mock_notification, mock_save):
        product = Product(
            security_gate_passed=None,
        )
        check_security_gate(product)
        self.assertIsNone(product.security_gate_passed)
        mock_save.assert_called_once()
        mock_notification.assert_called_once()
