from unittest.mock import patch

from unittests.base_test_case import BaseTestCase
from application.access_control.services.roles_permissions import Permissions, Roles
from application.core.api.serializers import ProductSerializer
from application.core.models import Observation, Product_Member


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
            current_severity=Observation.SEVERITY_CRITICAL,
            current_status=Observation.STATUS_OPEN,
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
            current_severity=Observation.SEVERITY_HIGH,
            current_status=Observation.STATUS_OPEN,
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
            current_severity=Observation.SEVERITY_MEDIUM,
            current_status=Observation.STATUS_OPEN,
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
            current_severity=Observation.SEVERITY_LOW,
            current_status=Observation.STATUS_OPEN,
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
            current_severity=Observation.SEVERITY_NONE,
            current_status=Observation.STATUS_OPEN,
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
            current_severity=Observation.SEVERITY_UNKOWN,
            current_status=Observation.STATUS_OPEN,
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
