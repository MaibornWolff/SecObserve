from datetime import timedelta
from unittest.mock import patch

from django.core.management import call_command
from django.utils import timezone
from rest_framework.test import APIClient

from application.access_control.models import User
from application.metrics.models import Product_Metrics
from unittests.base_test_case import BaseTestCase


class APITest:
    def __init__(
        self,
        username: str,
        method: str,
        url: str,
        post_data: str,
        expected_status_code: int,
        expected_data: str,
    ) -> None:
        self.username = username
        self.method = method
        self.url = url
        self.post_data = post_data
        self.expected_status_code = expected_status_code
        self.expected_data = expected_data


class TestAuthentication(BaseTestCase):
    patch.TEST_PREFIX = (
        "test",
        "setUp",
    )

    @classmethod
    @patch("application.core.signals.get_current_user")
    def setUpClass(self, mock_user):
        mock_user.return_value = None
        call_command("loaddata", "unittests/fixtures/unittests_fixtures.json")

        product_metrics = Product_Metrics.objects.get(pk=1)
        product_metrics.date = timezone.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        ) - timedelta(days=1)
        product_metrics.save()
        product_metrics = Product_Metrics.objects.get(pk=2)
        product_metrics.date = timezone.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        product_metrics.save()
        product_metrics = Product_Metrics.objects.get(pk=3)
        product_metrics.date = timezone.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        ) - timedelta(days=1)
        product_metrics.save()
        product_metrics = Product_Metrics.objects.get(pk=4)
        product_metrics.date = timezone.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        product_metrics.save()

        self.maxDiff = None
        super().setUpClass()

    @patch(
        "application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate"
    )
    def _test_api(self, data: APITest, mock_authentication):
        user_internal_write = User.objects.get(username=data.username)
        mock_authentication.return_value = user_internal_write, None

        api_client = APIClient()
        if data.method.lower() == "delete":
            response = api_client.delete(data.url)
        elif data.method.lower() == "get":
            response = api_client.get(data.url)
        elif data.method.lower() == "patch":
            response = api_client.patch(data.url, data.post_data, format="json")
        elif data.method.lower() == "post":
            response = api_client.post(data.url, data.post_data, format="json")
        elif data.method.lower() == "put":
            response = api_client.put(data.url, data.post_data, format="json")
        else:
            raise Exception(f"Unkown method: {data.method}")

        self.assertEqual(data.expected_status_code, response.status_code)
        if data.expected_data:
            self.assertEqual(data.expected_data, str(response.data))

    @patch(
        "application.access_control.services.api_token_authentication.APITokenAuthentication.authenticate"
    )
    def test_authorization(self, mock_authentication):
        user_internal_write = User.objects.get(username="db_internal_write")
        mock_authentication.return_value = user_internal_write, None

        # --- api_configurations ---

        expected_data = "OrderedDict([('count', 2), ('next', None), ('previous', None), ('results', [OrderedDict([('id', 1), ('product_data', OrderedDict([('id', 1), ('permissions', {<Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}), ('name', 'db_product_internal'), ('description', ''), ('repository_prefix', ''), ('security_gate_passed', True), ('security_gate_active', None), ('security_gate_threshold_critical', None), ('security_gate_threshold_high', None), ('security_gate_threshold_medium', None), ('security_gate_threshold_low', None), ('security_gate_threshold_none', None), ('security_gate_threshold_unkown', None), ('apply_general_rules', True), ('notification_ms_teams_webhook', ''), ('notification_email_to', ''), ('issue_tracker_active', False), ('issue_tracker_type', ''), ('issue_tracker_base_url', ''), ('issue_tracker_api_key', ''), ('issue_tracker_project_id', ''), ('issue_tracker_labels', ''), ('last_observation_change', '2022-12-16T17:13:18.283000+01:00'), ('product_group', None), ('repository_default_branch', 1), ('members', [2, 3])])), ('name', 'db_api_configuration_internal'), ('base_url', 'http://localhost:8080'), ('project_key', 'secobserve'), ('api_key', '__secret__'), ('product', 1), ('parser', 2)]), OrderedDict([('id', 2), ('product_data', OrderedDict([('id', 2), ('permissions', {<Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}), ('name', 'db_product_external'), ('description', ''), ('repository_prefix', ''), ('security_gate_passed', None), ('security_gate_active', False), ('security_gate_threshold_critical', None), ('security_gate_threshold_high', None), ('security_gate_threshold_medium', None), ('security_gate_threshold_low', None), ('security_gate_threshold_none', None), ('security_gate_threshold_unkown', None), ('apply_general_rules', True), ('notification_ms_teams_webhook', ''), ('notification_email_to', ''), ('issue_tracker_active', False), ('issue_tracker_type', ''), ('issue_tracker_base_url', ''), ('issue_tracker_api_key', ''), ('issue_tracker_project_id', ''), ('issue_tracker_labels', ''), ('last_observation_change', '2022-12-16T17:13:18.283000+01:00'), ('product_group', None), ('repository_default_branch', 3), ('members', [3, 4, 5])])), ('name', 'db_api_configuration_external'), ('base_url', 'http://localhost:8080'), ('project_key', 'secobserve'), ('api_key', '__secret__'), ('product', 2), ('parser', 2)])])])"
        self._test_api(
            APITest(
                "db_admin", "get", "/api/api_configurations/", None, 200, expected_data
            )
        )

        expected_data = "OrderedDict([('count', 1), ('next', None), ('previous', None), ('results', [OrderedDict([('id', 1), ('product_data', OrderedDict([('id', 1), ('permissions', {<Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}), ('name', 'db_product_internal'), ('description', ''), ('repository_prefix', ''), ('security_gate_passed', True), ('security_gate_active', None), ('security_gate_threshold_critical', None), ('security_gate_threshold_high', None), ('security_gate_threshold_medium', None), ('security_gate_threshold_low', None), ('security_gate_threshold_none', None), ('security_gate_threshold_unkown', None), ('apply_general_rules', True), ('notification_ms_teams_webhook', ''), ('notification_email_to', ''), ('issue_tracker_active', False), ('issue_tracker_type', ''), ('issue_tracker_base_url', ''), ('issue_tracker_api_key', ''), ('issue_tracker_project_id', ''), ('issue_tracker_labels', ''), ('last_observation_change', '2022-12-16T17:13:18.283000+01:00'), ('product_group', None), ('repository_default_branch', 1), ('members', [2, 3])])), ('name', 'db_api_configuration_internal'), ('base_url', 'http://localhost:8080'), ('project_key', 'secobserve'), ('api_key', '__secret__'), ('product', 1), ('parser', 2)])])])"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/api_configurations/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'id': 1, 'product_data': OrderedDict([('id', 1), ('permissions', {<Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}), ('name', 'db_product_internal'), ('description', ''), ('repository_prefix', ''), ('security_gate_passed', True), ('security_gate_active', None), ('security_gate_threshold_critical', None), ('security_gate_threshold_high', None), ('security_gate_threshold_medium', None), ('security_gate_threshold_low', None), ('security_gate_threshold_none', None), ('security_gate_threshold_unkown', None), ('apply_general_rules', True), ('notification_ms_teams_webhook', ''), ('notification_email_to', ''), ('issue_tracker_active', False), ('issue_tracker_type', ''), ('issue_tracker_base_url', ''), ('issue_tracker_api_key', ''), ('issue_tracker_project_id', ''), ('issue_tracker_labels', ''), ('last_observation_change', '2022-12-16T17:13:18.283000+01:00'), ('product_group', None), ('repository_default_branch', 1), ('members', [2, 3])]), 'name': 'db_api_configuration_internal', 'base_url': 'http://localhost:8080', 'project_key': 'secobserve', 'api_key': '__secret__', 'product': 1, 'parser': 2}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/api_configurations/1/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'message': 'No Api_Configuration matches the given query.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/api_configurations/2/",
                None,
                404,
                expected_data,
            )
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/api_configurations/99999/",
                None,
                404,
                expected_data,
            )
        )

        post_data = {
            "test_connection": False,
            "name": "string",
            "base_url": "string",
            "project_key": "string",
            "api_key": "string",
            "product": 1,
            "parser": 2,
        }
        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "post",
                "/api/api_configurations/",
                post_data,
                403,
                expected_data,
            )
        )
        expected_data = "{'id': 3, 'product_data': OrderedDict([('id', 1), ('permissions', {<Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}), ('name', 'db_product_internal'), ('description', ''), ('repository_prefix', ''), ('security_gate_passed', True), ('security_gate_active', None), ('security_gate_threshold_critical', None), ('security_gate_threshold_high', None), ('security_gate_threshold_medium', None), ('security_gate_threshold_low', None), ('security_gate_threshold_none', None), ('security_gate_threshold_unkown', None), ('apply_general_rules', True), ('notification_ms_teams_webhook', ''), ('notification_email_to', ''), ('issue_tracker_active', False), ('issue_tracker_type', ''), ('issue_tracker_base_url', ''), ('issue_tracker_api_key', ''), ('issue_tracker_project_id', ''), ('issue_tracker_labels', ''), ('last_observation_change', '2022-12-16T17:13:18.283000+01:00'), ('product_group', None), ('repository_default_branch', 1), ('members', [2, 3])]), 'name': 'string', 'base_url': 'string', 'project_key': 'string', 'api_key': 'string', 'product': 1, 'parser': 2}"
        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/api_configurations/",
                post_data,
                201,
                expected_data,
            )
        )

        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "patch",
                "/api/api_configurations/1/",
                {"name": "changed"},
                403,
                expected_data,
            )
        )
        expected_data = "{'id': 1, 'product_data': OrderedDict([('id', 1), ('permissions', {<Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}), ('name', 'db_product_internal'), ('description', ''), ('repository_prefix', ''), ('security_gate_passed', True), ('security_gate_active', None), ('security_gate_threshold_critical', None), ('security_gate_threshold_high', None), ('security_gate_threshold_medium', None), ('security_gate_threshold_low', None), ('security_gate_threshold_none', None), ('security_gate_threshold_unkown', None), ('apply_general_rules', True), ('notification_ms_teams_webhook', ''), ('notification_email_to', ''), ('issue_tracker_active', False), ('issue_tracker_type', ''), ('issue_tracker_base_url', ''), ('issue_tracker_api_key', ''), ('issue_tracker_project_id', ''), ('issue_tracker_labels', ''), ('last_observation_change', '2022-12-16T17:13:18.283000+01:00'), ('product_group', None), ('repository_default_branch', 1), ('members', [2, 3])]), 'name': 'changed', 'base_url': 'http://localhost:8080', 'project_key': 'secobserve', 'api_key': '__secret__', 'product': 1, 'parser': 2}"
        self._test_api(
            APITest(
                "db_internal_write",
                "patch",
                "/api/api_configurations/1/",
                {"name": "changed"},
                200,
                expected_data,
            )
        )

        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "delete",
                "/api/api_configurations/1/",
                None,
                403,
                expected_data,
            )
        )
        expected_data = "None"
        self._test_api(
            APITest(
                "db_internal_write",
                "delete",
                "/api/api_configurations/1/",
                None,
                204,
                expected_data,
            )
        )

        # --- general_rules ---

        expected_data = "OrderedDict([('count', 1), ('next', None), ('previous', None), ('results', [OrderedDict([('id', 3), ('name', 'db_general_rule'), ('description', ''), ('scanner_prefix', ''), ('title', ''), ('origin_component_name_version', ''), ('origin_docker_image_name_tag', ''), ('origin_endpoint_url', ''), ('origin_service_name', ''), ('origin_source_file', ''), ('new_severity', ''), ('new_status', ''), ('enabled', True), ('parser', 1)])])])"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/general_rules/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'message': 'No Rule matches the given query.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/general_rules/1/",
                None,
                404,
                expected_data,
            )
        )
        expected_data = "{'id': 3, 'name': 'db_general_rule', 'description': '', 'scanner_prefix': '', 'title': '', 'origin_component_name_version': '', 'origin_docker_image_name_tag': '', 'origin_endpoint_url': '', 'origin_service_name': '', 'origin_source_file': '', 'new_severity': '', 'new_status': '', 'enabled': True, 'parser': 1}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/general_rules/3/",
                None,
                200,
                expected_data,
            )
        )

        post_data = {"name": "string", "parser": 1}
        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/general_rules/",
                post_data,
                403,
                expected_data,
            )
        )
        expected_data = "{'id': 4, 'name': 'string', 'description': '', 'scanner_prefix': '', 'title': '', 'origin_component_name_version': '', 'origin_docker_image_name_tag': '', 'origin_endpoint_url': '', 'origin_service_name': '', 'origin_source_file': '', 'new_severity': '', 'new_status': '', 'enabled': True, 'parser': 1}"
        self._test_api(
            APITest(
                "db_admin", "post", "/api/general_rules/", post_data, 201, expected_data
            )
        )

        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "patch",
                "/api/general_rules/3/",
                {"name": "changed"},
                403,
                expected_data,
            )
        )
        expected_data = "{'id': 3, 'name': 'changed', 'description': '', 'scanner_prefix': '', 'title': '', 'origin_component_name_version': '', 'origin_docker_image_name_tag': '', 'origin_endpoint_url': '', 'origin_service_name': '', 'origin_source_file': '', 'new_severity': '', 'new_status': '', 'enabled': True, 'parser': 1}"
        self._test_api(
            APITest(
                "db_admin",
                "patch",
                "/api/general_rules/3/",
                {"name": "changed"},
                200,
                expected_data,
            )
        )

        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "delete",
                "/api/general_rules/3/",
                None,
                403,
                expected_data,
            )
        )
        expected_data = "None"
        self._test_api(
            APITest(
                "db_admin", "delete", "/api/general_rules/3/", None, 204, expected_data
            )
        )

        # --- metrics ---

        yesterday = (timezone.now() - timedelta(days=1)).date().isoformat()
        today = timezone.now().date().isoformat()

        expected_data = "{'open_critical': 7, 'open_high': 9, 'open_medium': 11, 'open_low': 13, 'open_none': 15, 'open_unknown': 17, 'open': 19, 'resolved': 21, 'duplicate': 23, 'false_positive': 25, 'in_review': 27, 'not_affected': 29, 'not_security': 31, 'risk_accepted': 33}"
        self._test_api(
            APITest(
                "db_admin",
                "get",
                "/api/metrics/product_metrics_current/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'2023-07-09': {'open_critical': 5, 'open_high': 7, 'open_medium': 9, 'open_low': 11, 'open_none': 13, 'open_unknown': 15, 'open': 17, 'resolved': 19, 'duplicate': 21, 'false_positive': 23, 'in_review': 25, 'not_affected': 27, 'not_security': 29, 'risk_accepted': 31}, '2023-07-10': {'open_critical': 7, 'open_high': 9, 'open_medium': 11, 'open_low': 13, 'open_none': 15, 'open_unknown': 17, 'open': 19, 'resolved': 21, 'duplicate': 23, 'false_positive': 25, 'in_review': 27, 'not_affected': 29, 'not_security': 31, 'risk_accepted': 33}}"
        expected_data = expected_data.replace("2023-07-10", today)
        expected_data = expected_data.replace("2023-07-09", yesterday)
        self._test_api(
            APITest(
                "db_admin",
                "get",
                "/api/metrics/product_metrics_timeline/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'open_critical': 2, 'open_high': 3, 'open_medium': 4, 'open_low': 5, 'open_none': 6, 'open_unknown': 7, 'open': 8, 'resolved': 9, 'duplicate': 10, 'false_positive': 11, 'in_review': 12, 'not_affected': 13, 'not_security': 14, 'risk_accepted': 15}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/metrics/product_metrics_current/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'2023-07-09': {'open_critical': 1, 'open_high': 2, 'open_medium': 3, 'open_low': 4, 'open_none': 5, 'open_unknown': 6, 'open': 7, 'resolved': 8, 'duplicate': 9, 'false_positive': 10, 'in_review': 11, 'not_affected': 12, 'not_security': 13, 'risk_accepted': 14}, '2023-07-10': {'open_critical': 2, 'open_high': 3, 'open_medium': 4, 'open_low': 5, 'open_none': 6, 'open_unknown': 7, 'open': 8, 'resolved': 9, 'duplicate': 10, 'false_positive': 11, 'in_review': 12, 'not_affected': 13, 'not_security': 14, 'risk_accepted': 15}}"
        expected_data = expected_data.replace("2023-07-10", today)
        expected_data = expected_data.replace("2023-07-09", yesterday)
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/metrics/product_metrics_timeline/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'open_critical': 2, 'open_high': 3, 'open_medium': 4, 'open_low': 5, 'open_none': 6, 'open_unknown': 7, 'open': 8, 'resolved': 9, 'duplicate': 10, 'false_positive': 11, 'in_review': 12, 'not_affected': 13, 'not_security': 14, 'risk_accepted': 15}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/metrics/product_metrics_current/?product_id=1",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'2023-07-09': {'open_critical': 1, 'open_high': 2, 'open_medium': 3, 'open_low': 4, 'open_none': 5, 'open_unknown': 6, 'open': 7, 'resolved': 8, 'duplicate': 9, 'false_positive': 10, 'in_review': 11, 'not_affected': 12, 'not_security': 13, 'risk_accepted': 14}, '2023-07-10': {'open_critical': 2, 'open_high': 3, 'open_medium': 4, 'open_low': 5, 'open_none': 6, 'open_unknown': 7, 'open': 8, 'resolved': 9, 'duplicate': 10, 'false_positive': 11, 'in_review': 12, 'not_affected': 13, 'not_security': 14, 'risk_accepted': 15}}"
        expected_data = expected_data.replace("2023-07-10", today)
        expected_data = expected_data.replace("2023-07-09", yesterday)
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/metrics/product_metrics_timeline/?product_id=1",
                None,
                200,
                expected_data,
            )
        )

        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/metrics/product_metrics_current/?product_id=2",
                None,
                403,
                expected_data,
            )
        )
        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/metrics/product_metrics_timeline/?product_id=2",
                None,
                403,
                expected_data,
            )
        )

        # --- observations ---

        expected_data = "OrderedDict([('count', 2), ('next', None), ('previous', None), ('results', [OrderedDict([('id', 1), ('product_data', OrderedDict([('id', 1), ('name', 'db_product_internal'), ('description', ''), ('repository_prefix', ''), ('security_gate_passed', True), ('security_gate_active', None), ('security_gate_threshold_critical', None), ('security_gate_threshold_high', None), ('security_gate_threshold_medium', None), ('security_gate_threshold_low', None), ('security_gate_threshold_none', None), ('security_gate_threshold_unkown', None), ('apply_general_rules', True), ('notification_ms_teams_webhook', ''), ('notification_email_to', ''), ('issue_tracker_active', False), ('issue_tracker_type', ''), ('issue_tracker_base_url', ''), ('issue_tracker_api_key', ''), ('issue_tracker_project_id', ''), ('issue_tracker_labels', ''), ('last_observation_change', '2022-12-16T17:13:18.283000+01:00'), ('product_group', None), ('repository_default_branch', 1)])), ('branch_name', 'db_branch_internal_dev'), ('parser_data', OrderedDict([('id', 1), ('name', 'db_parser_file'), ('type', 'DAST'), ('source', 'File')])), ('scanner_name', 'db_parser'), ('origin_component_name_version', ''), ('title', 'db_observation_internal'), ('description', ''), ('recommendation', ''), ('current_severity', 'Medium'), ('parser_severity', 'Medium'), ('rule_severity', ''), ('assessment_severity', ''), ('current_status', 'Duplicate'), ('parser_status', 'Open'), ('rule_status', 'Duplicate'), ('assessment_status', ''), ('scanner_observation_id', ''), ('vulnerability_id', ''), ('origin_component_name', ''), ('origin_component_version', ''), ('origin_component_purl', ''), ('origin_component_cpe', ''), ('origin_docker_image_name', ''), ('origin_docker_image_tag', ''), ('origin_docker_image_name_tag', ''), ('origin_docker_image_name_tag_short', ''), ('origin_endpoint_url', ''), ('origin_endpoint_scheme', ''), ('origin_endpoint_hostname', ''), ('origin_endpoint_port', None), ('origin_endpoint_path', ''), ('origin_endpoint_params', ''), ('origin_endpoint_query', ''), ('origin_endpoint_fragment', ''), ('origin_service_name', ''), ('origin_source_file', ''), ('origin_source_line_start', None), ('origin_source_line_end', None), ('cvss3_score', None), ('cvss3_vector', ''), ('cwe', None), ('epss_score', None), ('epss_percentile', None), ('found', None), ('scanner', 'db_parser'), ('upload_filename', 'parser.json'), ('api_configuration_name', ''), ('import_last_seen', '2022-12-15T17:14:20.870000+01:00'), ('created', '2022-12-15T17:10:35.513000+01:00'), ('modified', '2022-12-16T17:13:18.282000+01:00'), ('last_observation_log', '2022-12-16T17:13:18.281000+01:00'), ('identity_hash', '6eef8088480aa2523aeeb64ad35f876a942cc3172cfb36752f3a052a4f88642c'), ('issue_tracker_issue_id', ''), ('product', 1), ('branch', 1), ('parser', 1), ('general_rule', None), ('product_rule', 1)]), OrderedDict([('id', 2), ('product_data', OrderedDict([('id', 2), ('name', 'db_product_external'), ('description', ''), ('repository_prefix', ''), ('security_gate_passed', None), ('security_gate_active', False), ('security_gate_threshold_critical', None), ('security_gate_threshold_high', None), ('security_gate_threshold_medium', None), ('security_gate_threshold_low', None), ('security_gate_threshold_none', None), ('security_gate_threshold_unkown', None), ('apply_general_rules', True), ('notification_ms_teams_webhook', ''), ('notification_email_to', ''), ('issue_tracker_active', False), ('issue_tracker_type', ''), ('issue_tracker_base_url', ''), ('issue_tracker_api_key', ''), ('issue_tracker_project_id', ''), ('issue_tracker_labels', ''), ('last_observation_change', '2022-12-16T17:13:18.283000+01:00'), ('product_group', None), ('repository_default_branch', 3)])), ('branch_name', ''), ('parser_data', OrderedDict([('id', 1), ('name', 'db_parser_file'), ('type', 'DAST'), ('source', 'File')])), ('scanner_name', 'db_parser'), ('origin_component_name_version', ''), ('title', 'db_observation_internal'), ('description', ''), ('recommendation', ''), ('current_severity', 'Medium'), ('parser_severity', 'Medium'), ('rule_severity', ''), ('assessment_severity', ''), ('current_status', 'False positive'), ('parser_status', 'Open'), ('rule_status', 'False positive'), ('assessment_status', ''), ('scanner_observation_id', ''), ('vulnerability_id', ''), ('origin_component_name', ''), ('origin_component_version', ''), ('origin_component_purl', ''), ('origin_component_cpe', ''), ('origin_docker_image_name', ''), ('origin_docker_image_tag', ''), ('origin_docker_image_name_tag', ''), ('origin_docker_image_name_tag_short', ''), ('origin_endpoint_url', ''), ('origin_endpoint_scheme', ''), ('origin_endpoint_hostname', ''), ('origin_endpoint_port', None), ('origin_endpoint_path', ''), ('origin_endpoint_params', ''), ('origin_endpoint_query', ''), ('origin_endpoint_fragment', ''), ('origin_service_name', ''), ('origin_source_file', ''), ('origin_source_line_start', None), ('origin_source_line_end', None), ('cvss3_score', None), ('cvss3_vector', ''), ('cwe', None), ('epss_score', None), ('epss_percentile', None), ('found', None), ('scanner', 'db_parser'), ('upload_filename', 'parser.json'), ('api_configuration_name', ''), ('import_last_seen', '2022-12-15T17:14:20.876000+01:00'), ('created', '2022-12-15T17:10:35.521000+01:00'), ('modified', '2022-12-16T17:13:18.283000+01:00'), ('last_observation_log', '2022-12-16T17:13:18.283000+01:00'), ('identity_hash', 'bc8e59b7687fe3533616b3914c636389c131eac3bdbda1b67d8d26f890a74007'), ('issue_tracker_issue_id', ''), ('product', 2), ('branch', None), ('parser', 1), ('general_rule', None), ('product_rule', 2)])])])"
        self._test_api(
            APITest("db_admin", "get", "/api/observations/", None, 200, expected_data)
        )

        expected_data = "OrderedDict([('count', 1), ('next', None), ('previous', None), ('results', [OrderedDict([('id', 1), ('product_data', OrderedDict([('id', 1), ('name', 'db_product_internal'), ('description', ''), ('repository_prefix', ''), ('security_gate_passed', True), ('security_gate_active', None), ('security_gate_threshold_critical', None), ('security_gate_threshold_high', None), ('security_gate_threshold_medium', None), ('security_gate_threshold_low', None), ('security_gate_threshold_none', None), ('security_gate_threshold_unkown', None), ('apply_general_rules', True), ('notification_ms_teams_webhook', ''), ('notification_email_to', ''), ('issue_tracker_active', False), ('issue_tracker_type', ''), ('issue_tracker_base_url', ''), ('issue_tracker_api_key', ''), ('issue_tracker_project_id', ''), ('issue_tracker_labels', ''), ('last_observation_change', '2022-12-16T17:13:18.283000+01:00'), ('product_group', None), ('repository_default_branch', 1)])), ('branch_name', 'db_branch_internal_dev'), ('parser_data', OrderedDict([('id', 1), ('name', 'db_parser_file'), ('type', 'DAST'), ('source', 'File')])), ('scanner_name', 'db_parser'), ('origin_component_name_version', ''), ('title', 'db_observation_internal'), ('description', ''), ('recommendation', ''), ('current_severity', 'Medium'), ('parser_severity', 'Medium'), ('rule_severity', ''), ('assessment_severity', ''), ('current_status', 'Duplicate'), ('parser_status', 'Open'), ('rule_status', 'Duplicate'), ('assessment_status', ''), ('scanner_observation_id', ''), ('vulnerability_id', ''), ('origin_component_name', ''), ('origin_component_version', ''), ('origin_component_purl', ''), ('origin_component_cpe', ''), ('origin_docker_image_name', ''), ('origin_docker_image_tag', ''), ('origin_docker_image_name_tag', ''), ('origin_docker_image_name_tag_short', ''), ('origin_endpoint_url', ''), ('origin_endpoint_scheme', ''), ('origin_endpoint_hostname', ''), ('origin_endpoint_port', None), ('origin_endpoint_path', ''), ('origin_endpoint_params', ''), ('origin_endpoint_query', ''), ('origin_endpoint_fragment', ''), ('origin_service_name', ''), ('origin_source_file', ''), ('origin_source_line_start', None), ('origin_source_line_end', None), ('cvss3_score', None), ('cvss3_vector', ''), ('cwe', None), ('epss_score', None), ('epss_percentile', None), ('found', None), ('scanner', 'db_parser'), ('upload_filename', 'parser.json'), ('api_configuration_name', ''), ('import_last_seen', '2022-12-15T17:14:20.870000+01:00'), ('created', '2022-12-15T17:10:35.513000+01:00'), ('modified', '2022-12-16T17:13:18.282000+01:00'), ('last_observation_log', '2022-12-16T17:13:18.281000+01:00'), ('identity_hash', '6eef8088480aa2523aeeb64ad35f876a942cc3172cfb36752f3a052a4f88642c'), ('issue_tracker_issue_id', ''), ('product', 1), ('branch', 1), ('parser', 1), ('general_rule', None), ('product_rule', 1)])])])"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/observations/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'id': 1, 'product_data': OrderedDict([('id', 1), ('permissions', {<Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}), ('name', 'db_product_internal'), ('description', ''), ('repository_prefix', ''), ('security_gate_passed', True), ('security_gate_active', None), ('security_gate_threshold_critical', None), ('security_gate_threshold_high', None), ('security_gate_threshold_medium', None), ('security_gate_threshold_low', None), ('security_gate_threshold_none', None), ('security_gate_threshold_unkown', None), ('apply_general_rules', True), ('notification_ms_teams_webhook', ''), ('notification_email_to', ''), ('issue_tracker_active', False), ('issue_tracker_type', ''), ('issue_tracker_base_url', ''), ('issue_tracker_api_key', ''), ('issue_tracker_project_id', ''), ('issue_tracker_labels', ''), ('last_observation_change', '2022-12-16T17:13:18.283000+01:00'), ('product_group', None), ('repository_default_branch', 1), ('members', [2, 3])]), 'branch_name': 'db_branch_internal_dev', 'parser_data': OrderedDict([('id', 1), ('name', 'db_parser_file'), ('type', 'DAST'), ('source', 'File')]), 'observation_logs': [OrderedDict([('id', 2), ('severity', ''), ('status', 'Duplicate'), ('comment', 'Set by product rule'), ('created', '2022-12-15T17:10:35.524000+01:00'), ('user', 2)]), OrderedDict([('id', 1), ('severity', 'Medium'), ('status', 'Open'), ('comment', 'Set by parser'), ('created', '2022-12-15T17:10:35.518000+01:00'), ('user', 2)])], 'references': [], 'evidences': [OrderedDict([('id', 1), ('name', 'db_evidence_internal')])], 'origin_source_file_url': None, 'issue_tracker_issue_url': None, 'title': 'db_observation_internal', 'description': '', 'recommendation': '', 'current_severity': 'Medium', 'parser_severity': 'Medium', 'rule_severity': '', 'assessment_severity': '', 'current_status': 'Duplicate', 'parser_status': 'Open', 'rule_status': 'Duplicate', 'assessment_status': '', 'scanner_observation_id': '', 'vulnerability_id': '', 'origin_component_name': '', 'origin_component_version': '', 'origin_component_name_version': '', 'origin_component_purl': '', 'origin_component_cpe': '', 'origin_docker_image_name': '', 'origin_docker_image_tag': '', 'origin_docker_image_name_tag': '', 'origin_docker_image_name_tag_short': '', 'origin_endpoint_url': '', 'origin_endpoint_scheme': '', 'origin_endpoint_hostname': '', 'origin_endpoint_port': None, 'origin_endpoint_path': '', 'origin_endpoint_params': '', 'origin_endpoint_query': '', 'origin_endpoint_fragment': '', 'origin_service_name': '', 'origin_source_file': '', 'origin_source_line_start': None, 'origin_source_line_end': None, 'cvss3_score': None, 'cvss3_vector': '', 'cwe': None, 'epss_score': None, 'epss_percentile': None, 'found': None, 'scanner': 'db_parser', 'upload_filename': 'parser.json', 'api_configuration_name': '', 'import_last_seen': '2022-12-15T17:14:20.870000+01:00', 'created': '2022-12-15T17:10:35.513000+01:00', 'modified': '2022-12-16T17:13:18.282000+01:00', 'last_observation_log': '2022-12-16T17:13:18.281000+01:00', 'identity_hash': '6eef8088480aa2523aeeb64ad35f876a942cc3172cfb36752f3a052a4f88642c', 'issue_tracker_issue_id': '', 'product': 1, 'branch': 1, 'parser': 1, 'general_rule': None, 'product_rule': 1}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/observations/1/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'message': 'No Observation matches the given query.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/observations/2/",
                None,
                404,
                expected_data,
            )
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/observations/99999/",
                None,
                404,
                expected_data,
            )
        )

        post_data = {"product": 1}
        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "post",
                "/api/observations/",
                post_data,
                403,
                expected_data,
            )
        )
        expected_data = "{'message': 'Title: This field is required.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/observations/",
                post_data,
                400,
                expected_data,
            )
        )

        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "patch",
                "/api/observations/1/",
                {"title": "changed"},
                403,
                expected_data,
            )
        )
        expected_data = (
            "{'message': 'Non field errors: Only manual observations can be updated'}"
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "patch",
                "/api/observations/1/",
                {"title": "changed"},
                400,
                expected_data,
            )
        )

        post_data = {"comment": "reason for assessment"}
        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "patch",
                "/api/observations/1/assessment/",
                post_data,
                403,
                expected_data,
            )
        )
        expected_data = "{'message': 'Observation 99999 not found'}"
        self._test_api(
            APITest(
                "db_internal_read",
                "patch",
                "/api/observations/99999/assessment/",
                post_data,
                404,
                expected_data,
            )
        )
        expected_data = "None"
        self._test_api(
            APITest(
                "db_internal_write",
                "patch",
                "/api/observations/1/assessment/",
                post_data,
                200,
                expected_data,
            )
        )

        post_data = {"comment": "reason for assessment removal"}
        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "patch",
                "/api/observations/1/remove_assessment/",
                post_data,
                403,
                expected_data,
            )
        )
        expected_data = "{'message': 'Observation 99999 not found'}"
        self._test_api(
            APITest(
                "db_internal_read",
                "patch",
                "/api/observations/99999/remove_assessment/",
                post_data,
                404,
                expected_data,
            )
        )
        expected_data = "None"
        self._test_api(
            APITest(
                "db_internal_write",
                "patch",
                "/api/observations/1/remove_assessment/",
                post_data,
                200,
                expected_data,
            )
        )

        # --- evidences ---

        expected_data = "{'id': 1, 'product': 1, 'name': 'db_evidence_internal', 'evidence': 'abc', 'observation': 1}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/evidences/1/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'message': 'No Evidence matches the given query.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/evidences/2/",
                None,
                404,
                expected_data,
            )
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/evidences/99999/",
                None,
                404,
                expected_data,
            )
        )

        # --- product_members ---

        expected_data = "OrderedDict([('count', 4), ('next', None), ('previous', None), ('results', [OrderedDict([('id', 1), ('user_data', OrderedDict([('id', 2), ('username', 'db_internal_write'), ('first_name', ''), ('last_name', ''), ('full_name', 'db_internal_write'), ('email', ''), ('is_active', True), ('is_superuser', False), ('is_external', False), ('setting_theme', 'light'), ('permissions', [<Permissions.Product_Create: 1104>, <Permissions.Product_Group_Create: 1004>])])), ('role', 5), ('product', 1), ('user', 2)]), OrderedDict([('id', 2), ('user_data', OrderedDict([('id', 3), ('username', 'db_internal_read'), ('first_name', ''), ('last_name', ''), ('full_name', 'db_internal_read'), ('email', ''), ('is_active', True), ('is_superuser', False), ('is_external', False), ('setting_theme', 'light'), ('permissions', [<Permissions.Product_Create: 1104>, <Permissions.Product_Group_Create: 1004>])])), ('role', 1), ('product', 1), ('user', 3)]), OrderedDict([('id', 3), ('user_data', OrderedDict([('id', 4), ('username', 'db_external'), ('first_name', ''), ('last_name', ''), ('full_name', 'db_external'), ('email', ''), ('is_active', True), ('is_superuser', False), ('is_external', True), ('setting_theme', 'light'), ('permissions', [])])), ('role', 5), ('product', 2), ('user', 4)]), OrderedDict([('id', 4), ('user_data', OrderedDict([('id', 3), ('username', 'db_internal_read'), ('first_name', ''), ('last_name', ''), ('full_name', 'db_internal_read'), ('email', ''), ('is_active', True), ('is_superuser', False), ('is_external', False), ('setting_theme', 'light'), ('permissions', [<Permissions.Product_Create: 1104>, <Permissions.Product_Group_Create: 1004>])])), ('role', 1), ('product', 2), ('user', 3)])])])"
        self._test_api(
            APITest(
                "db_admin", "get", "/api/product_members/", None, 200, expected_data
            )
        )

        expected_data = "OrderedDict([('count', 2), ('next', None), ('previous', None), ('results', [OrderedDict([('id', 1), ('user_data', OrderedDict([('id', 2), ('username', 'db_internal_write'), ('first_name', ''), ('last_name', ''), ('full_name', 'db_internal_write'), ('email', ''), ('is_active', True), ('is_superuser', False), ('is_external', False), ('setting_theme', 'light'), ('permissions', [<Permissions.Product_Create: 1104>, <Permissions.Product_Group_Create: 1004>])])), ('role', 5), ('product', 1), ('user', 2)]), OrderedDict([('id', 2), ('user_data', OrderedDict([('id', 3), ('username', 'db_internal_read'), ('first_name', ''), ('last_name', ''), ('full_name', 'db_internal_read'), ('email', ''), ('is_active', True), ('is_superuser', False), ('is_external', False), ('setting_theme', 'light'), ('permissions', [<Permissions.Product_Create: 1104>, <Permissions.Product_Group_Create: 1004>])])), ('role', 1), ('product', 1), ('user', 3)])])])"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/product_members/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'id': 1, 'user_data': OrderedDict([('id', 2), ('username', 'db_internal_write'), ('first_name', ''), ('last_name', ''), ('full_name', 'db_internal_write'), ('email', ''), ('is_active', True), ('is_superuser', False), ('is_external', False), ('setting_theme', 'light'), ('permissions', [<Permissions.Product_Create: 1104>, <Permissions.Product_Group_Create: 1004>])]), 'role': 5, 'product': 1, 'user': 2}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/product_members/1/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'message': 'No Product_Member matches the given query.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/product_members/3/",
                None,
                404,
                expected_data,
            )
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/product_members/99999/",
                None,
                404,
                expected_data,
            )
        )

        post_data = {"role": 3, "product": 1, "user": 1}
        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "post",
                "/api/product_members/",
                post_data,
                403,
                expected_data,
            )
        )
        expected_data = "{'id': 6, 'user_data': OrderedDict([('id', 1), ('username', 'db_admin'), ('first_name', ''), ('last_name', ''), ('full_name', 'db_admin'), ('email', ''), ('is_active', True), ('is_superuser', True), ('is_external', False), ('setting_theme', 'light'), ('permissions', [<Permissions.Product_Create: 1104>, <Permissions.Product_Group_Create: 1004>])]), 'role': 3, 'product': 1, 'user': 1}"
        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/product_members/",
                post_data,
                201,
                expected_data,
            )
        )

        post_data = {"role": 2}
        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "patch",
                "/api/product_members/6/",
                post_data,
                403,
                expected_data,
            )
        )

        expected_data = "{'id': 6, 'user_data': OrderedDict([('id', 1), ('username', 'db_admin'), ('first_name', ''), ('last_name', ''), ('full_name', 'db_admin'), ('email', ''), ('is_active', True), ('is_superuser', True), ('is_external', False), ('setting_theme', 'light'), ('permissions', [<Permissions.Product_Create: 1104>, <Permissions.Product_Group_Create: 1004>])]), 'role': 2, 'product': 1, 'user': 1}"
        self._test_api(
            APITest(
                "db_internal_write",
                "patch",
                "/api/product_members/6/",
                post_data,
                200,
                expected_data,
            )
        )

        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "delete",
                "/api/product_members/6/",
                None,
                403,
                expected_data,
            )
        )
        expected_data = "None"
        self._test_api(
            APITest(
                "db_internal_write",
                "delete",
                "/api/product_members/6/",
                None,
                204,
                expected_data,
            )
        )

        # --- branches ---

        expected_data = "OrderedDict([('count', 3), ('next', None), ('previous', None), ('results', [OrderedDict([('id', 1), ('is_default_branch', True), ('open_critical_observation_count', 0), ('open_high_observation_count', 0), ('open_medium_observation_count', 0), ('open_low_observation_count', 0), ('open_none_observation_count', 0), ('open_unkown_observation_count', 0), ('name', 'db_branch_internal_dev'), ('product', 1)]), OrderedDict([('id', 2), ('is_default_branch', False), ('open_critical_observation_count', 0), ('open_high_observation_count', 0), ('open_medium_observation_count', 0), ('open_low_observation_count', 0), ('open_none_observation_count', 0), ('open_unkown_observation_count', 0), ('name', 'db_branch_internal_main'), ('product', 1)]), OrderedDict([('id', 3), ('is_default_branch', True), ('open_critical_observation_count', 0), ('open_high_observation_count', 0), ('open_medium_observation_count', 0), ('open_low_observation_count', 0), ('open_none_observation_count', 0), ('open_unkown_observation_count', 0), ('name', 'db_branch_external'), ('product', 2)])])])"
        self._test_api(
            APITest("db_admin", "get", "/api/branches/", None, 200, expected_data)
        )

        expected_data = "OrderedDict([('count', 2), ('next', None), ('previous', None), ('results', [OrderedDict([('id', 1), ('is_default_branch', True), ('open_critical_observation_count', 0), ('open_high_observation_count', 0), ('open_medium_observation_count', 0), ('open_low_observation_count', 0), ('open_none_observation_count', 0), ('open_unkown_observation_count', 0), ('name', 'db_branch_internal_dev'), ('product', 1)]), OrderedDict([('id', 2), ('is_default_branch', False), ('open_critical_observation_count', 0), ('open_high_observation_count', 0), ('open_medium_observation_count', 0), ('open_low_observation_count', 0), ('open_none_observation_count', 0), ('open_unkown_observation_count', 0), ('name', 'db_branch_internal_main'), ('product', 1)])])])"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/branches/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'id': 1, 'is_default_branch': True, 'open_critical_observation_count': 0, 'open_high_observation_count': 0, 'open_medium_observation_count': 0, 'open_low_observation_count': 0, 'open_none_observation_count': 0, 'open_unkown_observation_count': 0, 'name': 'db_branch_internal_dev', 'product': 1}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/branches/1/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'message': 'No Branch matches the given query.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/branches/3/",
                None,
                404,
                expected_data,
            )
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/branches/99999/",
                None,
                404,
                expected_data,
            )
        )

        post_data = {"name": "string", "product": 1}
        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "post",
                "/api/branches/",
                post_data,
                403,
                expected_data,
            )
        )

        expected_data = "{'id': 4, 'is_default_branch': False, 'open_critical_observation_count': 0, 'open_high_observation_count': 0, 'open_medium_observation_count': 0, 'open_low_observation_count': 0, 'open_none_observation_count': 0, 'open_unkown_observation_count': 0, 'name': 'string', 'product': 1}"
        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/branches/",
                post_data,
                201,
                expected_data,
            )
        )

        post_data = {"name": "changed"}
        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "patch",
                "/api/branches/1/",
                post_data,
                403,
                expected_data,
            )
        )
        expected_data = "{'id': 1, 'is_default_branch': True, 'open_critical_observation_count': 0, 'open_high_observation_count': 0, 'open_medium_observation_count': 0, 'open_low_observation_count': 0, 'open_none_observation_count': 0, 'open_unkown_observation_count': 0, 'name': 'changed', 'product': 1}"
        self._test_api(
            APITest(
                "db_internal_write",
                "patch",
                "/api/branches/1/",
                post_data,
                200,
                expected_data,
            )
        )

        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "delete",
                "/api/branches/1/",
                None,
                403,
                expected_data,
            )
        )
        expected_data = "{'message': \"Cannot delete some instances of model 'Branch' because they are referenced through protected foreign keys\"}"
        self._test_api(
            APITest(
                "db_internal_write",
                "delete",
                "/api/branches/1/",
                None,
                409,
                expected_data,
            )
        )

        # --- product_rules ---

        expected_data = "OrderedDict([('count', 2), ('next', None), ('previous', None), ('results', [OrderedDict([('id', 1), ('product_data', OrderedDict([('id', 1), ('permissions', {<Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}), ('name', 'db_product_internal'), ('description', ''), ('repository_prefix', ''), ('security_gate_passed', True), ('security_gate_active', None), ('security_gate_threshold_critical', None), ('security_gate_threshold_high', None), ('security_gate_threshold_medium', None), ('security_gate_threshold_low', None), ('security_gate_threshold_none', None), ('security_gate_threshold_unkown', None), ('apply_general_rules', True), ('notification_ms_teams_webhook', ''), ('notification_email_to', ''), ('issue_tracker_active', False), ('issue_tracker_type', ''), ('issue_tracker_base_url', ''), ('issue_tracker_api_key', ''), ('issue_tracker_project_id', ''), ('issue_tracker_labels', ''), ('last_observation_change', '2022-12-16T17:13:18.283000+01:00'), ('product_group', None), ('repository_default_branch', 1), ('members', [2, 3])])), ('name', 'db_product_rule_internal'), ('description', ''), ('scanner_prefix', ''), ('title', ''), ('origin_component_name_version', ''), ('origin_docker_image_name_tag', ''), ('origin_endpoint_url', ''), ('origin_service_name', ''), ('origin_source_file', ''), ('new_severity', ''), ('new_status', 'Duplicate'), ('enabled', True), ('product', 1), ('parser', 1)]), OrderedDict([('id', 2), ('product_data', OrderedDict([('id', 2), ('permissions', {<Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}), ('name', 'db_product_external'), ('description', ''), ('repository_prefix', ''), ('security_gate_passed', None), ('security_gate_active', False), ('security_gate_threshold_critical', None), ('security_gate_threshold_high', None), ('security_gate_threshold_medium', None), ('security_gate_threshold_low', None), ('security_gate_threshold_none', None), ('security_gate_threshold_unkown', None), ('apply_general_rules', True), ('notification_ms_teams_webhook', ''), ('notification_email_to', ''), ('issue_tracker_active', False), ('issue_tracker_type', ''), ('issue_tracker_base_url', ''), ('issue_tracker_api_key', ''), ('issue_tracker_project_id', ''), ('issue_tracker_labels', ''), ('last_observation_change', '2022-12-16T17:13:18.283000+01:00'), ('product_group', None), ('repository_default_branch', 3), ('members', [3, 4, 5])])), ('name', 'db_product_rule_external'), ('description', ''), ('scanner_prefix', ''), ('title', ''), ('origin_component_name_version', ''), ('origin_docker_image_name_tag', ''), ('origin_endpoint_url', ''), ('origin_service_name', ''), ('origin_source_file', ''), ('new_severity', ''), ('new_status', 'False positive'), ('enabled', True), ('product', 2), ('parser', 1)])])])"
        self._test_api(
            APITest("db_admin", "get", "/api/product_rules/", None, 200, expected_data)
        )

        expected_data = "OrderedDict([('count', 1), ('next', None), ('previous', None), ('results', [OrderedDict([('id', 1), ('product_data', OrderedDict([('id', 1), ('permissions', {<Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}), ('name', 'db_product_internal'), ('description', ''), ('repository_prefix', ''), ('security_gate_passed', True), ('security_gate_active', None), ('security_gate_threshold_critical', None), ('security_gate_threshold_high', None), ('security_gate_threshold_medium', None), ('security_gate_threshold_low', None), ('security_gate_threshold_none', None), ('security_gate_threshold_unkown', None), ('apply_general_rules', True), ('notification_ms_teams_webhook', ''), ('notification_email_to', ''), ('issue_tracker_active', False), ('issue_tracker_type', ''), ('issue_tracker_base_url', ''), ('issue_tracker_api_key', ''), ('issue_tracker_project_id', ''), ('issue_tracker_labels', ''), ('last_observation_change', '2022-12-16T17:13:18.283000+01:00'), ('product_group', None), ('repository_default_branch', 1), ('members', [2, 3])])), ('name', 'db_product_rule_internal'), ('description', ''), ('scanner_prefix', ''), ('title', ''), ('origin_component_name_version', ''), ('origin_docker_image_name_tag', ''), ('origin_endpoint_url', ''), ('origin_service_name', ''), ('origin_source_file', ''), ('new_severity', ''), ('new_status', 'Duplicate'), ('enabled', True), ('product', 1), ('parser', 1)])])])"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/product_rules/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'id': 1, 'product_data': OrderedDict([('id', 1), ('permissions', {<Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}), ('name', 'db_product_internal'), ('description', ''), ('repository_prefix', ''), ('security_gate_passed', True), ('security_gate_active', None), ('security_gate_threshold_critical', None), ('security_gate_threshold_high', None), ('security_gate_threshold_medium', None), ('security_gate_threshold_low', None), ('security_gate_threshold_none', None), ('security_gate_threshold_unkown', None), ('apply_general_rules', True), ('notification_ms_teams_webhook', ''), ('notification_email_to', ''), ('issue_tracker_active', False), ('issue_tracker_type', ''), ('issue_tracker_base_url', ''), ('issue_tracker_api_key', ''), ('issue_tracker_project_id', ''), ('issue_tracker_labels', ''), ('last_observation_change', '2022-12-16T17:13:18.283000+01:00'), ('product_group', None), ('repository_default_branch', 1), ('members', [2, 3])]), 'name': 'db_product_rule_internal', 'description': '', 'scanner_prefix': '', 'title': '', 'origin_component_name_version': '', 'origin_docker_image_name_tag': '', 'origin_endpoint_url': '', 'origin_service_name': '', 'origin_source_file': '', 'new_severity': '', 'new_status': 'Duplicate', 'enabled': True, 'product': 1, 'parser': 1}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/product_rules/1/",
                None,
                200,
                expected_data,
            )
        )
        expected_data = "{'message': 'No Rule matches the given query.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/product_rules/3/",
                None,
                404,
                expected_data,
            )
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/product_rules/99999/",
                None,
                404,
                expected_data,
            )
        )

        post_data = {"name": "string", "product": 1, "parser": 1}
        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "post",
                "/api/product_rules/",
                post_data,
                403,
                expected_data,
            )
        )
        expected_data = "{'id': 5, 'product_data': OrderedDict([('id', 1), ('permissions', {<Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}), ('name', 'db_product_internal'), ('description', ''), ('repository_prefix', ''), ('security_gate_passed', True), ('security_gate_active', None), ('security_gate_threshold_critical', None), ('security_gate_threshold_high', None), ('security_gate_threshold_medium', None), ('security_gate_threshold_low', None), ('security_gate_threshold_none', None), ('security_gate_threshold_unkown', None), ('apply_general_rules', True), ('notification_ms_teams_webhook', ''), ('notification_email_to', ''), ('issue_tracker_active', False), ('issue_tracker_type', ''), ('issue_tracker_base_url', ''), ('issue_tracker_api_key', ''), ('issue_tracker_project_id', ''), ('issue_tracker_labels', ''), ('last_observation_change', '2022-12-16T17:13:18.283000+01:00'), ('product_group', None), ('repository_default_branch', 1), ('members', [2, 3])]), 'name': 'string', 'description': '', 'scanner_prefix': '', 'title': '', 'origin_component_name_version': '', 'origin_docker_image_name_tag': '', 'origin_endpoint_url': '', 'origin_service_name': '', 'origin_source_file': '', 'new_severity': '', 'new_status': '', 'enabled': True, 'product': 1, 'parser': 1}"
        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/product_rules/",
                post_data,
                201,
                expected_data,
            )
        )

        post_data = {"name": "changed"}
        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "patch",
                "/api/product_rules/1/",
                post_data,
                403,
                expected_data,
            )
        )
        expected_data = "{'id': 1, 'product_data': OrderedDict([('id', 1), ('permissions', {<Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}), ('name', 'db_product_internal'), ('description', ''), ('repository_prefix', ''), ('security_gate_passed', True), ('security_gate_active', None), ('security_gate_threshold_critical', None), ('security_gate_threshold_high', None), ('security_gate_threshold_medium', None), ('security_gate_threshold_low', None), ('security_gate_threshold_none', None), ('security_gate_threshold_unkown', None), ('apply_general_rules', True), ('notification_ms_teams_webhook', ''), ('notification_email_to', ''), ('issue_tracker_active', False), ('issue_tracker_type', ''), ('issue_tracker_base_url', ''), ('issue_tracker_api_key', ''), ('issue_tracker_project_id', ''), ('issue_tracker_labels', ''), ('last_observation_change', '2022-12-16T17:13:18.283000+01:00'), ('product_group', None), ('repository_default_branch', 1), ('members', [2, 3])]), 'name': 'changed', 'description': '', 'scanner_prefix': '', 'title': '', 'origin_component_name_version': '', 'origin_docker_image_name_tag': '', 'origin_endpoint_url': '', 'origin_service_name': '', 'origin_source_file': '', 'new_severity': '', 'new_status': 'Duplicate', 'enabled': True, 'product': 1, 'parser': 1}"
        self._test_api(
            APITest(
                "db_internal_write",
                "patch",
                "/api/product_rules/1/",
                post_data,
                200,
                expected_data,
            )
        )

        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "delete",
                "/api/product_rules/1/",
                None,
                403,
                expected_data,
            )
        )
        expected_data = "{'message': \"Cannot delete some instances of model 'Rule' because they are referenced through protected foreign keys\"}"
        self._test_api(
            APITest(
                "db_internal_write",
                "delete",
                "/api/product_rules/1/",
                None,
                409,
                expected_data,
            )
        )

        # --- product_api_tokens ---

        expected_data = (
            "{'results': [OrderedDict([('id', 2), ('role', <Roles.Upload: 2>)])]}"
        )
        self._test_api(
            APITest(
                "db_admin",
                "get",
                "/api/product_api_tokens/?product=2",
                None,
                200,
                expected_data,
            )
        )

        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/product_api_tokens/?product=2",
                None,
                403,
                None,
            )
        )

        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_external",
                "post",
                "/api/product_api_tokens/",
                {"id": 1, "role": 2},
                403,
                expected_data,
            )
        )

        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/product_api_tokens/",
                {"id": 1, "role": 2},
                201,
                None,
            )
        )

        expected_data = (
            "{'results': [OrderedDict([('id', 1), ('role', <Roles.Upload: 2>)])]}"
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/product_api_tokens/?product=1",
                None,
                200,
                expected_data,
            )
        )

        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_external",
                "delete",
                "/api/product_api_tokens/1/",
                None,
                403,
                expected_data,
            )
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "delete",
                "/api/product_api_tokens/1/",
                None,
                204,
                None,
            )
        )

        # --- notifications ---

        expected_data = "OrderedDict([('count', 6), ('next', None), ('previous', None), ('results', [OrderedDict([('id', 1), ('product_name', 'db_product_internal'), ('observation_title', 'db_observation_internal'), ('user_full_name', 'db_internal_write'), ('name', 'exception_internal'), ('created', '2022-12-15T17:10:35.518000+01:00'), ('message', 'message_exception_internal'), ('type', 'Exception'), ('function', ''), ('arguments', ''), ('user', 2), ('product', 1), ('observation', 1)]), OrderedDict([('id', 2), ('product_name', 'db_product_external'), ('observation_title', 'db_observation_internal'), ('user_full_name', 'db_external'), ('name', 'exception_external'), ('created', '2022-12-15T17:10:35.518000+01:00'), ('message', 'message_exception_external'), ('type', 'Exception'), ('function', ''), ('arguments', ''), ('user', 4), ('product', 2), ('observation', 2)]), OrderedDict([('id', 3), ('product_name', 'db_product_internal'), ('observation_title', 'db_observation_internal'), ('user_full_name', 'db_internal_write'), ('name', 'security_gate_internal'), ('created', '2022-12-15T17:10:35.518000+01:00'), ('message', ''), ('type', 'Security gate'), ('function', ''), ('arguments', ''), ('user', 2), ('product', 1), ('observation', 1)]), OrderedDict([('id', 4), ('product_name', 'db_product_external'), ('observation_title', 'db_observation_internal'), ('user_full_name', 'db_external'), ('name', 'security_gate_internal'), ('created', '2022-12-15T17:10:35.518000+01:00'), ('message', ''), ('type', 'Security gate'), ('function', ''), ('arguments', ''), ('user', 4), ('product', 2), ('observation', 2)]), OrderedDict([('id', 5), ('product_name', 'db_product_internal'), ('observation_title', 'db_observation_internal'), ('user_full_name', 'db_internal_write'), ('name', 'task_internal'), ('created', '2022-12-15T17:10:35.518000+01:00'), ('message', 'message_task_internal'), ('type', 'Task'), ('function', 'function_task_internal'), ('arguments', 'arguments_task_internal'), ('user', 2), ('product', 1), ('observation', 1)]), OrderedDict([('id', 6), ('product_name', 'db_product_external'), ('observation_title', 'db_observation_internal'), ('user_full_name', 'db_external'), ('name', 'task_external'), ('created', '2022-12-15T17:10:35.518000+01:00'), ('message', 'message_task_external'), ('type', 'Task'), ('function', 'function_task_external'), ('arguments', 'arguments_task_external'), ('user', 4), ('product', 2), ('observation', 2)])])])"
        self._test_api(
            APITest("db_admin", "get", "/api/notifications/", None, 200, expected_data)
        )

        expected_data = "OrderedDict([('count', 2), ('next', None), ('previous', None), ('results', [OrderedDict([('id', 3), ('product_name', 'db_product_internal'), ('observation_title', 'db_observation_internal'), ('user_full_name', 'db_internal_write'), ('name', 'security_gate_internal'), ('created', '2022-12-15T17:10:35.518000+01:00'), ('message', ''), ('type', 'Security gate'), ('function', ''), ('arguments', ''), ('user', 2), ('product', 1), ('observation', 1)]), OrderedDict([('id', 5), ('product_name', 'db_product_internal'), ('observation_title', 'db_observation_internal'), ('user_full_name', 'db_internal_write'), ('name', 'task_internal'), ('created', '2022-12-15T17:10:35.518000+01:00'), ('message', 'message_task_internal'), ('type', 'Task'), ('function', 'function_task_internal'), ('arguments', 'arguments_task_internal'), ('user', 2), ('product', 1), ('observation', 1)])])])"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/notifications/",
                None,
                200,
                expected_data,
            )
        )

        self._test_api(
            APITest(
                "db_internal_write", "get", "/api/notifications/1/", None, 404, None
            )
        )

        self._test_api(
            APITest(
                "db_internal_write", "get", "/api/notifications/3/", None, 200, None
            )
        )

        post_data = {"notifications": [1, 3, 5]}
        expected_data = "{'message': 'Some notifications do not exist'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/notifications/bulk_delete/",
                post_data,
                400,
                expected_data,
            )
        )

        post_data = {"notifications": [3, 5]}
        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/notifications/bulk_delete/",
                post_data,
                204,
                None,
            )
        )

        expected_data = "OrderedDict([('count', 0), ('next', None), ('previous', None), ('results', [])])"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/notifications/",
                None,
                200,
                expected_data,
            )
        )

        # --- product ---

        expected_data = "OrderedDict([('count', 2), ('next', None), ('previous', None), ('results', [OrderedDict([('id', 1), ('open_critical_observation_count', 0), ('open_high_observation_count', 0), ('open_medium_observation_count', 0), ('open_low_observation_count', 0), ('open_none_observation_count', 0), ('open_unkown_observation_count', 0), ('permissions', {<Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}), ('product_group_name', ''), ('repository_default_branch_name', 'changed'), ('name', 'db_product_internal'), ('description', ''), ('repository_prefix', ''), ('security_gate_passed', True), ('security_gate_active', None), ('security_gate_threshold_critical', None), ('security_gate_threshold_high', None), ('security_gate_threshold_medium', None), ('security_gate_threshold_low', None), ('security_gate_threshold_none', None), ('security_gate_threshold_unkown', None), ('apply_general_rules', True), ('notification_ms_teams_webhook', ''), ('notification_email_to', ''), ('issue_tracker_active', False), ('issue_tracker_type', ''), ('issue_tracker_base_url', ''), ('issue_tracker_api_key', ''), ('issue_tracker_project_id', ''), ('issue_tracker_labels', ''), ('last_observation_change', '2022-12-16T17:13:18.283000+01:00'), ('product_group', None), ('repository_default_branch', 1), ('members', [2, 3])]), OrderedDict([('id', 2), ('open_critical_observation_count', 0), ('open_high_observation_count', 0), ('open_medium_observation_count', 0), ('open_low_observation_count', 0), ('open_none_observation_count', 0), ('open_unkown_observation_count', 0), ('permissions', {<Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}), ('product_group_name', ''), ('repository_default_branch_name', 'db_branch_external'), ('name', 'db_product_external'), ('description', ''), ('repository_prefix', ''), ('security_gate_passed', None), ('security_gate_active', False), ('security_gate_threshold_critical', None), ('security_gate_threshold_high', None), ('security_gate_threshold_medium', None), ('security_gate_threshold_low', None), ('security_gate_threshold_none', None), ('security_gate_threshold_unkown', None), ('apply_general_rules', True), ('notification_ms_teams_webhook', ''), ('notification_email_to', ''), ('issue_tracker_active', False), ('issue_tracker_type', ''), ('issue_tracker_base_url', ''), ('issue_tracker_api_key', ''), ('issue_tracker_project_id', ''), ('issue_tracker_labels', ''), ('last_observation_change', '2022-12-16T17:13:18.283000+01:00'), ('product_group', None), ('repository_default_branch', 3), ('members', [3, 4, 5])])])])"
        self._test_api(
            APITest("db_admin", "get", "/api/products/", None, 200, expected_data)
        )

        expected_data = "OrderedDict([('count', 1), ('next', None), ('previous', None), ('results', [OrderedDict([('id', 1), ('open_critical_observation_count', 0), ('open_high_observation_count', 0), ('open_medium_observation_count', 0), ('open_low_observation_count', 0), ('open_none_observation_count', 0), ('open_unkown_observation_count', 0), ('permissions', {<Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}), ('product_group_name', ''), ('repository_default_branch_name', 'changed'), ('name', 'db_product_internal'), ('description', ''), ('repository_prefix', ''), ('security_gate_passed', True), ('security_gate_active', None), ('security_gate_threshold_critical', None), ('security_gate_threshold_high', None), ('security_gate_threshold_medium', None), ('security_gate_threshold_low', None), ('security_gate_threshold_none', None), ('security_gate_threshold_unkown', None), ('apply_general_rules', True), ('notification_ms_teams_webhook', ''), ('notification_email_to', ''), ('issue_tracker_active', False), ('issue_tracker_type', ''), ('issue_tracker_base_url', ''), ('issue_tracker_api_key', ''), ('issue_tracker_project_id', ''), ('issue_tracker_labels', ''), ('last_observation_change', '2022-12-16T17:13:18.283000+01:00'), ('product_group', None), ('repository_default_branch', 1), ('members', [2, 3])])])])"
        self._test_api(
            APITest(
                "db_internal_write", "get", "/api/products/", None, 200, expected_data
            )
        )
        expected_data = "{'id': 1, 'open_critical_observation_count': 0, 'open_high_observation_count': 0, 'open_medium_observation_count': 0, 'open_low_observation_count': 0, 'open_none_observation_count': 0, 'open_unkown_observation_count': 0, 'permissions': {<Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}, 'product_group_name': '', 'repository_default_branch_name': 'changed', 'name': 'db_product_internal', 'description': '', 'repository_prefix': '', 'security_gate_passed': True, 'security_gate_active': None, 'security_gate_threshold_critical': None, 'security_gate_threshold_high': None, 'security_gate_threshold_medium': None, 'security_gate_threshold_low': None, 'security_gate_threshold_none': None, 'security_gate_threshold_unkown': None, 'apply_general_rules': True, 'notification_ms_teams_webhook': '', 'notification_email_to': '', 'issue_tracker_active': False, 'issue_tracker_type': '', 'issue_tracker_base_url': '', 'issue_tracker_api_key': '', 'issue_tracker_project_id': '', 'issue_tracker_labels': '', 'last_observation_change': '2022-12-16T17:13:18.283000+01:00', 'product_group': None, 'repository_default_branch': 1, 'members': [2, 3]}"
        self._test_api(
            APITest(
                "db_internal_write", "get", "/api/products/1/", None, 200, expected_data
            )
        )
        expected_data = "{'message': 'No Product matches the given query.'}"
        self._test_api(
            APITest(
                "db_internal_write", "get", "/api/products/2/", None, 404, expected_data
            )
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/products/99999/",
                None,
                404,
                expected_data,
            )
        )

        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_external",
                "post",
                "/api/products/",
                {"name": "string"},
                403,
                expected_data,
            )
        )
        expected_data = "{'id': 3, 'open_critical_observation_count': 0, 'open_high_observation_count': 0, 'open_medium_observation_count': 0, 'open_low_observation_count': 0, 'open_none_observation_count': 0, 'open_unkown_observation_count': 0, 'permissions': {<Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}, 'product_group_name': '', 'repository_default_branch_name': '', 'name': 'string', 'description': '', 'repository_prefix': '', 'security_gate_passed': None, 'security_gate_active': None, 'security_gate_threshold_critical': None, 'security_gate_threshold_high': None, 'security_gate_threshold_medium': None, 'security_gate_threshold_low': None, 'security_gate_threshold_none': None, 'security_gate_threshold_unkown': None, 'apply_general_rules': True, 'notification_ms_teams_webhook': '', 'notification_email_to': '', 'issue_tracker_active': False, 'issue_tracker_type': '', 'issue_tracker_base_url': '', 'issue_tracker_api_key': '', 'issue_tracker_project_id': '', 'issue_tracker_labels': '', 'last_observation_change': '2022-12-16T17:13:18.283000+01:00', 'product_group': None, 'repository_default_branch': None, 'members': [2]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/products/",
                {
                    "name": "string",
                    "last_observation_change": "2022-12-16T17:13:18.283000+01:00",
                },
                201,
                expected_data,
            )
        )

        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "patch",
                "/api/products/1/",
                {"description": "string"},
                403,
                expected_data,
            )
        )
        expected_data = "{'id': 1, 'open_critical_observation_count': 0, 'open_high_observation_count': 0, 'open_medium_observation_count': 0, 'open_low_observation_count': 0, 'open_none_observation_count': 0, 'open_unkown_observation_count': 0, 'permissions': {<Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}, 'product_group_name': '', 'repository_default_branch_name': 'changed', 'name': 'db_product_internal', 'description': 'string', 'repository_prefix': '', 'security_gate_passed': True, 'security_gate_active': None, 'security_gate_threshold_critical': None, 'security_gate_threshold_high': None, 'security_gate_threshold_medium': None, 'security_gate_threshold_low': None, 'security_gate_threshold_none': None, 'security_gate_threshold_unkown': None, 'apply_general_rules': True, 'notification_ms_teams_webhook': '', 'notification_email_to': '', 'issue_tracker_active': False, 'issue_tracker_type': '', 'issue_tracker_base_url': '', 'issue_tracker_api_key': '', 'issue_tracker_project_id': '', 'issue_tracker_labels': '', 'last_observation_change': '2022-12-16T17:13:18.283000+01:00', 'product_group': None, 'repository_default_branch': 1, 'members': [2, 3]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "patch",
                "/api/products/1/",
                {"description": "string"},
                200,
                expected_data,
            )
        )

        post_data = None
        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "post",
                "/api/products/1/apply_rules/",
                post_data,
                403,
                expected_data,
            )
        )
        expected_data = "None"
        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/products/1/apply_rules/",
                post_data,
                204,
                expected_data,
            )
        )

        post_data = {
            "severity": "Critical",
            "status": "Open",
            "comment": "string",
            "observations": [],
        }
        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "post",
                "/api/products/1/observations_bulk_assessment/",
                post_data,
                403,
                expected_data,
            )
        )
        expected_data = "None"
        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/products/1/observations_bulk_assessment/",
                post_data,
                204,
                expected_data,
            )
        )

        post_data = {"observations": []}
        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "post",
                "/api/products/1/observations_bulk_delete/",
                post_data,
                403,
                expected_data,
            )
        )
        expected_data = "None"
        self._test_api(
            APITest(
                "db_internal_write",
                "post",
                "/api/products/1/observations_bulk_delete/",
                post_data,
                204,
                expected_data,
            )
        )

        expected_data = (
            "{'message': 'You do not have permission to perform this action.'}"
        )
        self._test_api(
            APITest(
                "db_internal_read",
                "delete",
                "/api/products/1/",
                None,
                403,
                expected_data,
            )
        )
        expected_data = "{'message': \"Cannot delete some instances of model 'Product' because they are referenced through protected foreign keys\"}"
        self._test_api(
            APITest(
                "db_internal_write",
                "delete",
                "/api/products/1/",
                None,
                409,
                expected_data,
            )
        )

        # --- users ---

        expected_data = "OrderedDict([('count', 4), ('next', None), ('previous', None), ('results', [OrderedDict([('id', 1), ('username', 'db_admin'), ('first_name', ''), ('last_name', ''), ('full_name', 'db_admin'), ('email', ''), ('is_active', True), ('is_superuser', True), ('is_external', False), ('setting_theme', 'light'), ('permissions', [<Permissions.Product_Create: 1104>, <Permissions.Product_Group_Create: 1004>])]), OrderedDict([('id', 2), ('username', 'db_internal_write'), ('first_name', ''), ('last_name', ''), ('full_name', 'db_internal_write'), ('email', ''), ('is_active', True), ('is_superuser', False), ('is_external', False), ('setting_theme', 'light'), ('permissions', [<Permissions.Product_Create: 1104>, <Permissions.Product_Group_Create: 1004>])]), OrderedDict([('id', 3), ('username', 'db_internal_read'), ('first_name', ''), ('last_name', ''), ('full_name', 'db_internal_read'), ('email', ''), ('is_active', True), ('is_superuser', False), ('is_external', False), ('setting_theme', 'light'), ('permissions', [<Permissions.Product_Create: 1104>, <Permissions.Product_Group_Create: 1004>])]), OrderedDict([('id', 4), ('username', 'db_external'), ('first_name', ''), ('last_name', ''), ('full_name', 'db_external'), ('email', ''), ('is_active', True), ('is_superuser', False), ('is_external', True), ('setting_theme', 'light'), ('permissions', [])])])])"
        self._test_api(
            APITest("db_admin", "get", "/api/users/", None, 200, expected_data)
        )

        expected_data = "OrderedDict([('count', 4), ('next', None), ('previous', None), ('results', [OrderedDict([('id', 1), ('username', 'db_admin'), ('first_name', ''), ('last_name', ''), ('full_name', 'db_admin'), ('email', ''), ('is_active', True), ('is_superuser', True), ('is_external', False), ('setting_theme', 'light'), ('permissions', [<Permissions.Product_Create: 1104>, <Permissions.Product_Group_Create: 1004>])]), OrderedDict([('id', 2), ('username', 'db_internal_write'), ('first_name', ''), ('last_name', ''), ('full_name', 'db_internal_write'), ('email', ''), ('is_active', True), ('is_superuser', False), ('is_external', False), ('setting_theme', 'light'), ('permissions', [<Permissions.Product_Create: 1104>, <Permissions.Product_Group_Create: 1004>])]), OrderedDict([('id', 3), ('username', 'db_internal_read'), ('first_name', ''), ('last_name', ''), ('full_name', 'db_internal_read'), ('email', ''), ('is_active', True), ('is_superuser', False), ('is_external', False), ('setting_theme', 'light'), ('permissions', [<Permissions.Product_Create: 1104>, <Permissions.Product_Group_Create: 1004>])]), OrderedDict([('id', 4), ('username', 'db_external'), ('first_name', ''), ('last_name', ''), ('full_name', 'db_external'), ('email', ''), ('is_active', True), ('is_superuser', False), ('is_external', True), ('setting_theme', 'light'), ('permissions', [])])])])"
        self._test_api(
            APITest("db_internal_write", "get", "/api/users/", None, 200, expected_data)
        )
        expected_data = "{'id': 1, 'username': 'db_admin', 'first_name': '', 'last_name': '', 'full_name': 'db_admin', 'email': '', 'is_active': True, 'is_superuser': True, 'is_external': False, 'setting_theme': 'light', 'permissions': [<Permissions.Product_Create: 1104>, <Permissions.Product_Group_Create: 1004>]}"
        self._test_api(
            APITest(
                "db_internal_write", "get", "/api/users/1/", None, 200, expected_data
            )
        )
        expected_data = "{'message': 'No User matches the given query.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/users/99999/",
                None,
                404,
                expected_data,
            )
        )

        expected_data = "OrderedDict([('count', 2), ('next', None), ('previous', None), ('results', [OrderedDict([('id', 3), ('username', 'db_internal_read'), ('first_name', ''), ('last_name', ''), ('full_name', 'db_internal_read'), ('email', ''), ('is_active', True), ('is_superuser', False), ('is_external', False), ('setting_theme', 'light'), ('permissions', [<Permissions.Product_Create: 1104>, <Permissions.Product_Group_Create: 1004>])]), OrderedDict([('id', 4), ('username', 'db_external'), ('first_name', ''), ('last_name', ''), ('full_name', 'db_external'), ('email', ''), ('is_active', True), ('is_superuser', False), ('is_external', True), ('setting_theme', 'light'), ('permissions', [])])])])"
        self._test_api(
            APITest("db_external", "get", "/api/users/", None, 200, expected_data)
        )
        expected_data = "{'id': 4, 'username': 'db_external', 'first_name': '', 'last_name': '', 'full_name': 'db_external', 'email': '', 'is_active': True, 'is_superuser': False, 'is_external': True, 'setting_theme': 'light', 'permissions': []}"
        self._test_api(
            APITest("db_external", "get", "/api/users/4/", None, 200, expected_data)
        )
        expected_data = "{'id': 3, 'username': 'db_internal_read', 'first_name': '', 'last_name': '', 'full_name': 'db_internal_read', 'email': '', 'is_active': True, 'is_superuser': False, 'is_external': False, 'setting_theme': 'light', 'permissions': [<Permissions.Product_Create: 1104>, <Permissions.Product_Group_Create: 1004>]}"
        self._test_api(
            APITest("db_external", "get", "/api/users/3/", None, 200, expected_data)
        )
        expected_data = "{'message': 'No User matches the given query.'}"
        self._test_api(
            APITest("db_external", "get", "/api/users/2/", None, 404, expected_data)
        )

        expected_data = "{'id': 2, 'username': 'db_internal_write', 'first_name': '', 'last_name': '', 'full_name': 'db_internal_write', 'email': '', 'is_active': True, 'is_superuser': False, 'is_external': False, 'setting_theme': 'light', 'permissions': [<Permissions.Product_Create: 1104>, <Permissions.Product_Group_Create: 1004>]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/users/me/",
                None,
                200,
                expected_data,
            )
        )

        post_data = {"setting_theme": "dark"}
        expected_data = "{'id': 2, 'username': 'db_internal_write', 'first_name': '', 'last_name': '', 'full_name': 'db_internal_write', 'email': '', 'is_active': True, 'is_superuser': False, 'is_external': False, 'setting_theme': 'dark', 'permissions': [<Permissions.Product_Create: 1104>, <Permissions.Product_Group_Create: 1004>]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "patch",
                "/api/users/my_settings/",
                post_data,
                200,
                expected_data,
            )
        )

        post_data = {"setting_theme": "medium"}
        expected_data = (
            "{'message': 'Setting theme: \"medium\" is not a valid choice.'}"
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "patch",
                "/api/users/my_settings/",
                post_data,
                400,
                expected_data,
            )
        )
