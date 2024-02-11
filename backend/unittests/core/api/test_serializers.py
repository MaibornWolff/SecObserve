from unittest.mock import patch

from rest_framework.serializers import ValidationError

from application.access_control.services.roles_permissions import Permissions, Roles
from application.core.api.serializers import BranchSerializer, ProductSerializer
from application.core.models import Product_Member
from application.core.types import Severity, Status
from unittests.base_test_case import BaseTestCase


class TestBranchSerializer(BaseTestCase):
    def test_is_default_branch_true(self):
        branch_serializer = BranchSerializer()
        self.assertTrue(branch_serializer.get_is_default_branch(obj=self.branch_1))

    def test_is_default_branch_false(self):
        branch_serializer = BranchSerializer()
        self.assertFalse(branch_serializer.get_is_default_branch(obj=self.branch_2))

    @patch("application.core.models.Observation.objects.filter")
    def test_get_open_critical_observation_count(self, mock_filter):
        mock_filter.return_value.count.return_value = 99
        branch_serializer = BranchSerializer()
        self.assertEqual(
            99,
            branch_serializer.get_open_critical_observation_count(obj=self.branch_1),
        )
        mock_filter.assert_called_with(
            branch=self.branch_1,
            current_severity=Severity.SEVERITY_CRITICAL,
            current_status=Status.STATUS_OPEN,
        )

    @patch("application.core.models.Observation.objects.filter")
    def test_get_open_high_observation_count(self, mock_filter):
        mock_filter.return_value.count.return_value = 99
        branch_serializer = BranchSerializer()
        self.assertEqual(
            99, branch_serializer.get_open_high_observation_count(obj=self.branch_1)
        )
        mock_filter.assert_called_with(
            branch=self.branch_1,
            current_severity=Severity.SEVERITY_HIGH,
            current_status=Status.STATUS_OPEN,
        )

    @patch("application.core.models.Observation.objects.filter")
    def test_get_open_medium_observation_count(self, mock_filter):
        mock_filter.return_value.count.return_value = 99
        branch_serializer = BranchSerializer()
        self.assertEqual(
            99, branch_serializer.get_open_medium_observation_count(obj=self.branch_1)
        )
        mock_filter.assert_called_with(
            branch=self.branch_1,
            current_severity=Severity.SEVERITY_MEDIUM,
            current_status=Status.STATUS_OPEN,
        )

    @patch("application.core.models.Observation.objects.filter")
    def test_get_open_low_observation_count(self, mock_filter):
        mock_filter.return_value.count.return_value = 99
        branch_serializer = BranchSerializer()
        self.assertEqual(
            99, branch_serializer.get_open_low_observation_count(obj=self.branch_1)
        )
        mock_filter.assert_called_with(
            branch=self.branch_1,
            current_severity=Severity.SEVERITY_LOW,
            current_status=Status.STATUS_OPEN,
        )

    @patch("application.core.models.Observation.objects.filter")
    def test_get_open_none_observation_count(self, mock_filter):
        mock_filter.return_value.count.return_value = 99
        branch_serializer = BranchSerializer()
        self.assertEqual(
            99, branch_serializer.get_open_none_observation_count(obj=self.branch_1)
        )
        mock_filter.assert_called_with(
            branch=self.branch_1,
            current_severity=Severity.SEVERITY_NONE,
            current_status=Status.STATUS_OPEN,
        )

    @patch("application.core.models.Observation.objects.filter")
    def test_get_open_unkown_observation_count(self, mock_filter):
        mock_filter.return_value.count.return_value = 99
        branch_serializer = BranchSerializer()
        self.assertEqual(
            99, branch_serializer.get_open_unkown_observation_count(obj=self.branch_1)
        )
        mock_filter.assert_called_with(
            branch=self.branch_1,
            current_severity=Severity.SEVERITY_UNKOWN,
            current_status=Status.STATUS_OPEN,
        )


class TestProductSerializer(BaseTestCase):
    @patch("application.core.models.Observation.objects.filter")
    def test_get_open_critical_observation_count(self, mock_filter):
        mock_filter.return_value.count.return_value = 99
        product_serializer = ProductSerializer()
        self.assertEqual(
            99,
            product_serializer.get_open_critical_observation_count(obj=self.product_1),
        )
        mock_filter.assert_called_with(
            product=self.product_1,
            branch=self.branch_1,
            current_severity=Severity.SEVERITY_CRITICAL,
            current_status=Status.STATUS_OPEN,
        )

    @patch("application.core.models.Observation.objects.filter")
    def test_get_open_high_observation_count(self, mock_filter):
        mock_filter.return_value.count.return_value = 99
        product_serializer = ProductSerializer()
        self.assertEqual(
            99, product_serializer.get_open_high_observation_count(obj=self.product_1)
        )
        mock_filter.assert_called_with(
            product=self.product_1,
            branch=self.branch_1,
            current_severity=Severity.SEVERITY_HIGH,
            current_status=Status.STATUS_OPEN,
        )

    @patch("application.core.models.Observation.objects.filter")
    def test_get_open_medium_observation_count(self, mock_filter):
        mock_filter.return_value.count.return_value = 99
        product_serializer = ProductSerializer()
        self.assertEqual(
            99, product_serializer.get_open_medium_observation_count(obj=self.product_1)
        )
        mock_filter.assert_called_with(
            product=self.product_1,
            branch=self.branch_1,
            current_severity=Severity.SEVERITY_MEDIUM,
            current_status=Status.STATUS_OPEN,
        )

    @patch("application.core.models.Observation.objects.filter")
    def test_get_open_low_observation_count(self, mock_filter):
        mock_filter.return_value.count.return_value = 99
        product_serializer = ProductSerializer()
        self.assertEqual(
            99, product_serializer.get_open_low_observation_count(obj=self.product_1)
        )
        mock_filter.assert_called_with(
            product=self.product_1,
            branch=self.branch_1,
            current_severity=Severity.SEVERITY_LOW,
            current_status=Status.STATUS_OPEN,
        )

    @patch("application.core.models.Observation.objects.filter")
    def test_get_open_none_observation_count(self, mock_filter):
        mock_filter.return_value.count.return_value = 99
        product_serializer = ProductSerializer()
        self.assertEqual(
            99, product_serializer.get_open_none_observation_count(obj=self.product_1)
        )
        mock_filter.assert_called_with(
            product=self.product_1,
            branch=self.branch_1,
            current_severity=Severity.SEVERITY_NONE,
            current_status=Status.STATUS_OPEN,
        )

    @patch("application.core.models.Observation.objects.filter")
    def test_get_open_unkown_observation_count(self, mock_filter):
        mock_filter.return_value.count.return_value = 99
        product_serializer = ProductSerializer()
        self.assertEqual(
            99, product_serializer.get_open_unkown_observation_count(obj=self.product_1)
        )
        mock_filter.assert_called_with(
            product=self.product_1,
            branch=self.branch_1,
            current_severity=Severity.SEVERITY_UNKOWN,
            current_status=Status.STATUS_OPEN,
        )

    @patch("application.core.api.serializers.get_current_user")
    @patch("application.core.api.serializers.get_permissions_for_role")
    def test_get_permissions_superuser(self, mock_permissions, mock_user):
        mock_permissions.return_value = [
            Permissions.Product_View,
            Permissions.Product_Edit,
            Permissions.Product_Delete,
        ]
        mock_user.return_value = self.user_admin
        product_serializer = ProductSerializer()
        self.assertEqual(
            [
                Permissions.Product_View,
                Permissions.Product_Edit,
                Permissions.Product_Delete,
            ],
            product_serializer.get_permissions(obj=self.product_1),
        )
        mock_permissions.assert_called_with(Roles.Owner)

    @patch("application.core.api.serializers.get_current_user")
    @patch("application.core.api.serializers.get_product_member")
    @patch("application.core.api.serializers.get_permissions_for_role")
    def test_get_permissions_user(
        self, mock_permissions, mock_product_member, mock_user
    ):
        mock_permissions.return_value = [Permissions.Product_View]
        mock_product_member.return_value = Product_Member(
            product=self.product_1, user=self.user_internal, role=Roles.Writer
        )
        mock_user.return_value = self.user_internal
        product_serializer = ProductSerializer()
        self.assertEqual(
            [Permissions.Product_View],
            product_serializer.get_permissions(obj=self.product_1),
        )
        mock_product_member.assert_called_with(self.product_1)
        mock_permissions.assert_called_with(Roles.Writer)

    @patch("application.core.api.serializers.get_current_user")
    @patch("application.core.api.serializers.get_product_member")
    @patch("application.core.api.serializers.get_permissions_for_role")
    def test_get_permissions_no_product_member(
        self, mock_permissions, mock_product_member, mock_user
    ):
        mock_user.return_value = self.user_external
        mock_product_member.return_value = None
        product_serializer = ProductSerializer()
        self.assertEqual([], product_serializer.get_permissions(obj=self.product_1))
        mock_product_member.assert_called_with(self.product_1)
        mock_permissions.assert_not_called()

    @patch("application.core.api.serializers.get_product_member")
    def test_validate_security_gate_active_empty(self, mock_product_member):
        self.product_1.security_gate_active = True
        self.product_1.security_gate_threshold_critical = None
        self.product_1.security_gate_threshold_high = None
        self.product_1.security_gate_threshold_medium = None
        self.product_1.security_gate_threshold_low = None
        self.product_1.security_gate_threshold_none = None
        self.product_1.security_gate_threshold_unkown = None
        product_serializer = ProductSerializer(self.product_1)

        data = product_serializer.validate(product_serializer.data)

        self.assertEqual(0, data["security_gate_threshold_critical"])
        self.assertEqual(0, data["security_gate_threshold_high"])
        self.assertEqual(0, data["security_gate_threshold_medium"])
        self.assertEqual(0, data["security_gate_threshold_low"])
        self.assertEqual(0, data["security_gate_threshold_none"])
        self.assertEqual(0, data["security_gate_threshold_unkown"])

    @patch("application.core.api.serializers.get_product_member")
    def test_validate_security_gate_active_full(self, mock_product_member):
        self.product_1.security_gate_active = True
        self.product_1.security_gate_threshold_critical = 1
        self.product_1.security_gate_threshold_high = 2
        self.product_1.security_gate_threshold_medium = 3
        self.product_1.security_gate_threshold_low = 4
        self.product_1.security_gate_threshold_none = 5
        self.product_1.security_gate_threshold_unkown = 6
        product_serializer = ProductSerializer(self.product_1)

        data = product_serializer.validate(product_serializer.data)

        self.assertEqual(1, data["security_gate_threshold_critical"])
        self.assertEqual(2, data["security_gate_threshold_high"])
        self.assertEqual(3, data["security_gate_threshold_medium"])
        self.assertEqual(4, data["security_gate_threshold_low"])
        self.assertEqual(5, data["security_gate_threshold_none"])
        self.assertEqual(6, data["security_gate_threshold_unkown"])

    def test_validate_repository_prefix_empty(self):
        self.product_1.repository_prefix = ""
        product_serializer = ProductSerializer(self.product_1)

        validated_data = product_serializer.run_validation(product_serializer.data)

        self.assertEqual("", validated_data["repository_prefix"])

    def test_validate_repository_prefix_invalid(self):
        self.product_1.repository_prefix = "invalid_url"
        product_serializer = ProductSerializer(self.product_1)

        with self.assertRaises(ValidationError) as e:
            product_serializer.run_validation(product_serializer.data)

        self.assertEqual(
            "{'repository_prefix': [ErrorDetail(string='Not a valid URL', code='invalid')]}",
            str(e.exception),
        )

    def test_validate_repository_prefix_valid(self):
        self.product_1.repository_prefix = "https://example.com"
        product_serializer = ProductSerializer(self.product_1)

        validated_data = product_serializer.run_validation(product_serializer.data)

        self.assertEqual("https://example.com", validated_data["repository_prefix"])

    def test_validate_notification_msteams_slack_invalid(self):
        self.product_1.notification_ms_teams_webhook = "invalid_url"
        self.product_1.notification_slack_webhook = "invalid_url"
        product_serializer = ProductSerializer(self.product_1)

        with self.assertRaises(ValidationError) as e:
            product_serializer.run_validation(product_serializer.data)

        self.assertEqual(
            "{'notification_ms_teams_webhook': [ErrorDetail(string='Not a valid URL', code='invalid')], 'notification_slack_webhook': [ErrorDetail(string='Not a valid URL', code='invalid')]}",
            str(e.exception),
        )
