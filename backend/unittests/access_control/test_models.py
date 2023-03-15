from unittest import TestCase
from unittest.mock import patch

from application.access_control.models import User


class TestUser(TestCase):
    @patch("django.contrib.auth.models.AbstractUser.save")
    def test_save_first_and_last_name(self, mock):
        user = User(first_name="first", last_name="last", username="user")
        user.save()

        self.assertEqual("first last", user.full_name)
        mock.assert_called()

    @patch("django.contrib.auth.models.AbstractUser.save")
    def test_save_first_name_only(self, mock):
        user = User(first_name="first", username="user")
        user.save()

        self.assertEqual("first", user.full_name)
        mock.assert_called()

    @patch("django.contrib.auth.models.AbstractUser.save")
    def test_save_last_name_only(self, mock):
        user = User(last_name="last", username="user")
        user.save()

        self.assertEqual("last", user.full_name)
        mock.assert_called()

    @patch("django.contrib.auth.models.AbstractUser.save")
    def test_save_no_name(self, mock):
        user = User(username="user")
        user.save()

        self.assertEqual("user", user.full_name)
        mock.assert_called()
