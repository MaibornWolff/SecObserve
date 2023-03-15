from unittest.mock import patch

from unittests.base_test_case import BaseTestCase
from application.access_control.models import JWT_Secret
from application.access_control.services.jwt_secret import get_secret, _create_secret


class TestJwtSecret(BaseTestCase):
    @patch("application.access_control.models.JWT_Secret.objects.all")
    def test_get_secret_one(self, mock):
        mock.return_value = [JWT_Secret(secret="secret")]
        self.assertEqual("secret", get_secret())
        mock.assert_called()

    @patch("application.access_control.models.JWT_Secret.objects.all")
    @patch("application.access_control.models.JWT_Secret.delete")
    @patch("application.access_control.models.JWT_Secret.save")
    @patch("application.access_control.services.jwt_secret._create_secret")
    def test_get_secret_none(
        self, create_secret_mock, save_mock, delete_mock, all_mock
    ):
        all_mock.return_value = []
        create_secret_mock.return_value = "secret"

        self.assertEqual("secret", get_secret())
        create_secret_mock.assert_called()
        save_mock.assert_called()
        delete_mock.assert_not_called()
        all_mock.assert_called()

    @patch("application.access_control.models.JWT_Secret.objects.all")
    @patch("application.access_control.models.JWT_Secret.delete")
    @patch("application.access_control.models.JWT_Secret.save")
    @patch("application.access_control.services.jwt_secret._create_secret")
    def test_get_secret_multiple(
        self, create_secret_mock, save_mock, delete_mock, all_mock
    ):
        all_mock.return_value = [
            JWT_Secret(secret="secret_1"),
            JWT_Secret(secret="secret_2"),
        ]
        create_secret_mock.return_value = "secret"

        self.assertEqual("secret", get_secret())
        create_secret_mock.assert_called()
        save_mock.assert_called()
        self.assertEqual(delete_mock.call_count, 2)
        all_mock.assert_called()

    def test_create_secret(self):
        secret = _create_secret()
        self.assertEqual(32, len(secret))
