from unittest.mock import patch

from rest_framework.serializers import ValidationError

from application.access_control.api.serializers import (
    AuthorizationGroupMemberSerializer,
)
from application.access_control.models import Authorization_Group
from unittests.base_test_case import BaseTestCase


class TestAuthorizationGroupMemberSerializer(BaseTestCase):
    def test_validate_authorization_group_change(self):
        auhorization_group_2 = Authorization_Group.objects.create(name="group_2")
        authorization_group_member_serializer = AuthorizationGroupMemberSerializer(self.authorization_group_member_1)
        attrs = {
            "authorization_group": auhorization_group_2,
        }

        with self.assertRaises(ValidationError) as e:
            authorization_group_member_serializer.validate(attrs)

        self.assertEqual(
            "[ErrorDetail(string='Authorization group and user cannot be changed', code='invalid')]",
            str(e.exception),
        )

    def test_validate_user_change(self):
        authorization_group_member_serializer = AuthorizationGroupMemberSerializer(self.authorization_group_member_1)
        attrs = {
            "user": self.user_external,
        }

        with self.assertRaises(ValidationError) as e:
            authorization_group_member_serializer.validate(attrs)

        self.assertEqual(
            "[ErrorDetail(string='Authorization group and user cannot be changed', code='invalid')]",
            str(e.exception),
        )

    @patch("application.access_control.api.serializers.get_authorization_group_member")
    def test_validate_already_exists(self, mock_authorization_group_member):
        mock_authorization_group_member.return_value = self.authorization_group_member_1
        authorization_group_member_serializer = AuthorizationGroupMemberSerializer()
        attrs = {
            "authorization_group": self.authorization_group_1,
            "user": self.user_internal,
        }

        with self.assertRaises(ValidationError) as e:
            authorization_group_member_serializer.validate(attrs)

        self.assertEqual(
            "[ErrorDetail(string='Authorization group member authorization_group_1 / user_internal@example.com already exists', code='invalid')]",
            str(e.exception),
        )
        mock_authorization_group_member.assert_called_with(self.authorization_group_1, self.user_internal)

    def test_validate_successful_with_instance(self):
        authorization_group_member_serializer = AuthorizationGroupMemberSerializer(self.authorization_group_member_1)
        attrs = {"is_manager": False}

        new_attrs = authorization_group_member_serializer.validate(attrs)

        self.assertEqual(new_attrs, attrs)

    @patch("application.access_control.api.serializers.get_authorization_group_member")
    def test_validate_successful_no_instance(self, mock_authorization_group_member):
        mock_authorization_group_member.return_value = None
        authorization_group_member_serializer = AuthorizationGroupMemberSerializer()
        attrs = {
            "authorization_group": self.authorization_group_1,
            "user": self.user_external,
            "is_manager": False,
        }

        new_attrs = authorization_group_member_serializer.validate(attrs)

        self.assertEqual(new_attrs, attrs)
        mock_authorization_group_member.assert_called_with(self.authorization_group_1, self.user_external)
