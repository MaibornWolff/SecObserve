from unittest.mock import patch

from application.access_control.models import JWT_Secret
from application.access_control.services.jwt_secret import create_secret
from unittests.base_test_case import BaseTestCase


class TestJwtSecret(BaseTestCase):
    def test_create_secret(self):
        secret = create_secret()
        self.assertEqual(32, len(secret))
