from datetime import date, timedelta

from application.commons.models import Settings
from application.core.models import Product
from application.core.services.risk_acceptance_expiry import (
    calculate_risk_acceptance_expiry_date,
)
from unittests.base_test_case import BaseTestCase


class TestCalculateRiskAcceptanceExpiryDate(BaseTestCase):

    def test_product_risk_acceptance_expiry_active_is_none(self):
        product = Product(risk_acceptance_expiry_active=None)
        product.product_group = Product(risk_acceptance_expiry_active=None)
        self.assertEqual(date.today() + timedelta(30), calculate_risk_acceptance_expiry_date(product))

    def test_product_risk_acceptance_expiry_active_is_false(self):
        product = Product(risk_acceptance_expiry_active=False)
        self.assertIsNone(calculate_risk_acceptance_expiry_date(product))

    def test_product_risk_acceptance_expiry_active_is_true_and_days_is_none(self):
        product = Product(risk_acceptance_expiry_active=True, risk_acceptance_expiry_days=None)
        self.assertEqual(date.today() + timedelta(30), calculate_risk_acceptance_expiry_date(product))

    def test_product_risk_acceptance_expiry_active_is_true_and_days_is_zero(self):
        product = Product(risk_acceptance_expiry_active=True, risk_acceptance_expiry_days=0)
        self.assertEqual(date.today() + timedelta(30), calculate_risk_acceptance_expiry_date(product))

    def test_product_risk_acceptance_expiry_active_is_true_and_days_is_positive(self):
        product = Product(risk_acceptance_expiry_active=True, risk_acceptance_expiry_days=1)
        self.assertEqual(date.today() + timedelta(1), calculate_risk_acceptance_expiry_date(product))

    def test_product_group_risk_acceptance_expiry_active_is_false(self):
        product = Product(risk_acceptance_expiry_active=None)
        product.product_group = Product(risk_acceptance_expiry_active=False)
        self.assertIsNone(calculate_risk_acceptance_expiry_date(product))

    def test_product_group_risk_acceptance_expiry_active_is_true_and_days_is_none(self):
        product = Product(risk_acceptance_expiry_active=None)
        product.product_group = Product(risk_acceptance_expiry_active=True, risk_acceptance_expiry_days=None)
        self.assertEqual(date.today() + timedelta(30), calculate_risk_acceptance_expiry_date(product))

    def test_product_group_risk_acceptance_expiry_active_is_true_and_days_is_zero(self):
        product = Product(risk_acceptance_expiry_active=None)
        product.product_group = Product(risk_acceptance_expiry_active=True, risk_acceptance_expiry_days=0)
        self.assertEqual(date.today() + timedelta(30), calculate_risk_acceptance_expiry_date(product))

    def test_product_group_risk_acceptance_expiry_active_is_true_and_days_is_positive(
        self,
    ):
        product = Product(risk_acceptance_expiry_active=None)
        product.product_group = Product(risk_acceptance_expiry_active=True, risk_acceptance_expiry_days=2)
        self.assertEqual(date.today() + timedelta(2), calculate_risk_acceptance_expiry_date(product))

    def test_settings_risk_acceptance_expiry_days_is_zero(self):
        product = Product(risk_acceptance_expiry_active=None)
        product.product_group = Product(risk_acceptance_expiry_active=None)
        settings = Settings.load()
        settings.risk_acceptance_expiry_days = 0
        settings.save()
        self.assertIsNone(calculate_risk_acceptance_expiry_date(product))
        settings.delete()
