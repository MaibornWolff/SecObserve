from unittests.access_control.api.test_authorization import (
    APITest,
    TestAuthorizationBase,
)


class TestAuthorizationProductRules(TestAuthorizationBase):
    def test_authorization_product_rules(self):
        expected_data = "OrderedDict({'count': 2, 'next': None, 'previous': None, 'results': [OrderedDict({'id': 1, 'product_data': OrderedDict({'id': 1, 'permissions': {<Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Service_View: 1501>, <Permissions.Service_Delete: 1503>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}, 'name': 'db_product_internal', 'description': '', 'repository_prefix': '', 'repository_branch_housekeeping_active': None, 'repository_branch_housekeeping_keep_inactive_days': None, 'repository_branch_housekeeping_exempt_branches': '', 'security_gate_passed': True, 'security_gate_active': None, 'security_gate_threshold_critical': None, 'security_gate_threshold_high': None, 'security_gate_threshold_medium': None, 'security_gate_threshold_low': None, 'security_gate_threshold_none': None, 'security_gate_threshold_unkown': None, 'apply_general_rules': True, 'notification_ms_teams_webhook': '', 'notification_slack_webhook': '', 'notification_email_to': '', 'issue_tracker_active': False, 'issue_tracker_type': '', 'issue_tracker_base_url': '', 'issue_tracker_username': '', 'issue_tracker_api_key': '', 'issue_tracker_project_id': '', 'issue_tracker_labels': '', 'issue_tracker_issue_type': '', 'issue_tracker_status_closed': '', 'issue_tracker_minimum_severity': '', 'last_observation_change': '2022-12-16T17:13:18.283000+01:00', 'product_group': 3, 'repository_default_branch': 1, 'members': [2, 3]}), 'name': 'db_product_rule_internal', 'description': '', 'scanner_prefix': '', 'title': '', 'description_observation': '', 'origin_component_name_version': '', 'origin_docker_image_name_tag': '', 'origin_endpoint_url': '', 'origin_service_name': '', 'origin_source_file': '', 'origin_cloud_qualified_resource': '', 'new_severity': '', 'new_status': 'Duplicate', 'enabled': True, 'product': 1, 'parser': 1}), OrderedDict({'id': 2, 'product_data': OrderedDict({'id': 2, 'permissions': {<Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Service_View: 1501>, <Permissions.Service_Delete: 1503>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}, 'name': 'db_product_external', 'description': '', 'repository_prefix': '', 'repository_branch_housekeeping_active': None, 'repository_branch_housekeeping_keep_inactive_days': None, 'repository_branch_housekeeping_exempt_branches': '', 'security_gate_passed': None, 'security_gate_active': False, 'security_gate_threshold_critical': None, 'security_gate_threshold_high': None, 'security_gate_threshold_medium': None, 'security_gate_threshold_low': None, 'security_gate_threshold_none': None, 'security_gate_threshold_unkown': None, 'apply_general_rules': True, 'notification_ms_teams_webhook': '', 'notification_slack_webhook': '', 'notification_email_to': '', 'issue_tracker_active': False, 'issue_tracker_type': '', 'issue_tracker_base_url': '', 'issue_tracker_username': '', 'issue_tracker_api_key': '', 'issue_tracker_project_id': '', 'issue_tracker_labels': '', 'issue_tracker_issue_type': '', 'issue_tracker_status_closed': '', 'issue_tracker_minimum_severity': '', 'last_observation_change': '2022-12-16T17:13:18.283000+01:00', 'product_group': None, 'repository_default_branch': 3, 'members': [3, 4, 5]}), 'name': 'db_product_rule_external', 'description': '', 'scanner_prefix': '', 'title': '', 'description_observation': '', 'origin_component_name_version': '', 'origin_docker_image_name_tag': '', 'origin_endpoint_url': '', 'origin_service_name': '', 'origin_source_file': '', 'origin_cloud_qualified_resource': '', 'new_severity': '', 'new_status': 'False positive', 'enabled': True, 'product': 2, 'parser': 1})]})"
        self._test_api(
            APITest("db_admin", "get", "/api/product_rules/", None, 200, expected_data)
        )

        expected_data = "OrderedDict({'count': 1, 'next': None, 'previous': None, 'results': [OrderedDict({'id': 1, 'product_data': OrderedDict({'id': 1, 'permissions': {<Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Service_View: 1501>, <Permissions.Service_Delete: 1503>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}, 'name': 'db_product_internal', 'description': '', 'repository_prefix': '', 'repository_branch_housekeeping_active': None, 'repository_branch_housekeeping_keep_inactive_days': None, 'repository_branch_housekeeping_exempt_branches': '', 'security_gate_passed': True, 'security_gate_active': None, 'security_gate_threshold_critical': None, 'security_gate_threshold_high': None, 'security_gate_threshold_medium': None, 'security_gate_threshold_low': None, 'security_gate_threshold_none': None, 'security_gate_threshold_unkown': None, 'apply_general_rules': True, 'notification_ms_teams_webhook': '', 'notification_slack_webhook': '', 'notification_email_to': '', 'issue_tracker_active': False, 'issue_tracker_type': '', 'issue_tracker_base_url': '', 'issue_tracker_username': '', 'issue_tracker_api_key': '', 'issue_tracker_project_id': '', 'issue_tracker_labels': '', 'issue_tracker_issue_type': '', 'issue_tracker_status_closed': '', 'issue_tracker_minimum_severity': '', 'last_observation_change': '2022-12-16T17:13:18.283000+01:00', 'product_group': 3, 'repository_default_branch': 1, 'members': [2, 3]}), 'name': 'db_product_rule_internal', 'description': '', 'scanner_prefix': '', 'title': '', 'description_observation': '', 'origin_component_name_version': '', 'origin_docker_image_name_tag': '', 'origin_endpoint_url': '', 'origin_service_name': '', 'origin_source_file': '', 'origin_cloud_qualified_resource': '', 'new_severity': '', 'new_status': 'Duplicate', 'enabled': True, 'product': 1, 'parser': 1})]})"
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

        expected_data = "{'id': 1, 'product_data': OrderedDict({'id': 1, 'permissions': {<Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Service_View: 1501>, <Permissions.Service_Delete: 1503>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}, 'name': 'db_product_internal', 'description': '', 'repository_prefix': '', 'repository_branch_housekeeping_active': None, 'repository_branch_housekeeping_keep_inactive_days': None, 'repository_branch_housekeeping_exempt_branches': '', 'security_gate_passed': True, 'security_gate_active': None, 'security_gate_threshold_critical': None, 'security_gate_threshold_high': None, 'security_gate_threshold_medium': None, 'security_gate_threshold_low': None, 'security_gate_threshold_none': None, 'security_gate_threshold_unkown': None, 'apply_general_rules': True, 'notification_ms_teams_webhook': '', 'notification_slack_webhook': '', 'notification_email_to': '', 'issue_tracker_active': False, 'issue_tracker_type': '', 'issue_tracker_base_url': '', 'issue_tracker_username': '', 'issue_tracker_api_key': '', 'issue_tracker_project_id': '', 'issue_tracker_labels': '', 'issue_tracker_issue_type': '', 'issue_tracker_status_closed': '', 'issue_tracker_minimum_severity': '', 'last_observation_change': '2022-12-16T17:13:18.283000+01:00', 'product_group': 3, 'repository_default_branch': 1, 'members': [2, 3]}), 'name': 'db_product_rule_internal', 'description': '', 'scanner_prefix': '', 'title': '', 'description_observation': '', 'origin_component_name_version': '', 'origin_docker_image_name_tag': '', 'origin_endpoint_url': '', 'origin_service_name': '', 'origin_source_file': '', 'origin_cloud_qualified_resource': '', 'new_severity': '', 'new_status': 'Duplicate', 'enabled': True, 'product': 1, 'parser': 1}"
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

        expected_data = "{'id': 4, 'product_data': OrderedDict({'id': 1, 'permissions': {<Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Service_View: 1501>, <Permissions.Service_Delete: 1503>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}, 'name': 'db_product_internal', 'description': '', 'repository_prefix': '', 'repository_branch_housekeeping_active': None, 'repository_branch_housekeeping_keep_inactive_days': None, 'repository_branch_housekeeping_exempt_branches': '', 'security_gate_passed': True, 'security_gate_active': None, 'security_gate_threshold_critical': None, 'security_gate_threshold_high': None, 'security_gate_threshold_medium': None, 'security_gate_threshold_low': None, 'security_gate_threshold_none': None, 'security_gate_threshold_unkown': None, 'apply_general_rules': True, 'notification_ms_teams_webhook': '', 'notification_slack_webhook': '', 'notification_email_to': '', 'issue_tracker_active': False, 'issue_tracker_type': '', 'issue_tracker_base_url': '', 'issue_tracker_username': '', 'issue_tracker_api_key': '', 'issue_tracker_project_id': '', 'issue_tracker_labels': '', 'issue_tracker_issue_type': '', 'issue_tracker_status_closed': '', 'issue_tracker_minimum_severity': '', 'last_observation_change': '2022-12-16T17:13:18.283000+01:00', 'product_group': 3, 'repository_default_branch': 1, 'members': [2, 3]}), 'name': 'string', 'description': '', 'scanner_prefix': '', 'title': '', 'description_observation': '', 'origin_component_name_version': '', 'origin_docker_image_name_tag': '', 'origin_endpoint_url': '', 'origin_service_name': '', 'origin_source_file': '', 'origin_cloud_qualified_resource': '', 'new_severity': '', 'new_status': '', 'enabled': True, 'product': 1, 'parser': 1}"
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

        post_data = {"name": "changed", "scanner_prefix": "also_changed"}
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

        expected_data = "{'id': 1, 'product_data': OrderedDict({'id': 1, 'permissions': {<Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Service_View: 1501>, <Permissions.Service_Delete: 1503>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}, 'name': 'db_product_internal', 'description': '', 'repository_prefix': '', 'repository_branch_housekeeping_active': None, 'repository_branch_housekeeping_keep_inactive_days': None, 'repository_branch_housekeeping_exempt_branches': '', 'security_gate_passed': True, 'security_gate_active': None, 'security_gate_threshold_critical': None, 'security_gate_threshold_high': None, 'security_gate_threshold_medium': None, 'security_gate_threshold_low': None, 'security_gate_threshold_none': None, 'security_gate_threshold_unkown': None, 'apply_general_rules': True, 'notification_ms_teams_webhook': '', 'notification_slack_webhook': '', 'notification_email_to': '', 'issue_tracker_active': False, 'issue_tracker_type': '', 'issue_tracker_base_url': '', 'issue_tracker_username': '', 'issue_tracker_api_key': '', 'issue_tracker_project_id': '', 'issue_tracker_labels': '', 'issue_tracker_issue_type': '', 'issue_tracker_status_closed': '', 'issue_tracker_minimum_severity': '', 'last_observation_change': '2022-12-16T17:13:18.283000+01:00', 'product_group': 3, 'repository_default_branch': 1, 'members': [2, 3]}), 'name': 'changed', 'description': '', 'scanner_prefix': 'also_changed', 'title': '', 'description_observation': '', 'origin_component_name_version': '', 'origin_docker_image_name_tag': '', 'origin_endpoint_url': '', 'origin_service_name': '', 'origin_source_file': '', 'origin_cloud_qualified_resource': '', 'new_severity': '', 'new_status': 'Duplicate', 'enabled': True, 'product': 1, 'parser': 1}"
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

        expected_data = (
            "{'message': 'Cannot delete Rule because it still has Observations.'}"
        )
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
