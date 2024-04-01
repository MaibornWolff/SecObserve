from unittests.access_control.api.test_authorization import (
    APITest,
    TestAuthorizationBase,
)
from unittests.access_control.services.test_authorization import (
    prepare_authorization_groups,
)


class TestAuthorizationOpenVEX_Product(TestAuthorizationBase):
    def test_authorization_openvex_product_member(self):
        self._test_authorization_openvex()

    def test_authorization_openvex_product_authorization_group_member(self):
        prepare_authorization_groups()
        self._test_authorization_openvex()

    def _test_authorization_openvex(self):
        expected_data = "{'count': 2, 'next': None, 'previous': None, 'results': [{'id': 1, 'product_data': {'id': 1, 'permissions': {<Permissions.VEX_View: 5001>, <Permissions.VEX_Edit: 5002>, <Permissions.VEX_Delete: 5003>, <Permissions.VEX_Create: 5004>, <Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Observation_Log_Approval: 2101>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_Authorization_Group_Member_View: 1601>, <Permissions.Product_Authorization_Group_Member_Edit: 1602>, <Permissions.Product_Authorization_Group_Member_Delete: 1603>, <Permissions.Product_Authorization_Group_Member_Create: 1604>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Service_View: 1501>, <Permissions.Service_Delete: 1503>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}, 'product_group_assessments_need_approval': False, 'name': 'db_product_internal', 'description': '', 'purl': '', 'cpe23': '', 'repository_prefix': '', 'repository_branch_housekeeping_active': None, 'repository_branch_housekeeping_keep_inactive_days': None, 'repository_branch_housekeeping_exempt_branches': '', 'security_gate_passed': True, 'security_gate_active': None, 'security_gate_threshold_critical': None, 'security_gate_threshold_high': None, 'security_gate_threshold_medium': None, 'security_gate_threshold_low': None, 'security_gate_threshold_none': None, 'security_gate_threshold_unkown': None, 'apply_general_rules': True, 'notification_ms_teams_webhook': '', 'notification_slack_webhook': '', 'notification_email_to': '', 'issue_tracker_active': False, 'issue_tracker_type': '', 'issue_tracker_base_url': '', 'issue_tracker_username': '', 'issue_tracker_api_key': '', 'issue_tracker_project_id': '', 'issue_tracker_labels': '', 'issue_tracker_issue_type': '', 'issue_tracker_status_closed': '', 'issue_tracker_minimum_severity': '', 'last_observation_change': '2022-12-16T17:13:18.283000+01:00', 'assessments_need_approval': False, 'product_group': 3, 'repository_default_branch': 1}, 'vulnerability_names': 'CVE_vulnerability_1', 'branch_names': 'db_branch_internal_dev', 'user_full_name': 'db_external', 'document_id_prefix': 'openvex_prefix', 'document_base_id': '2024_0001', 'version': 1, 'content_hash': 'abcdef123456', 'id_namespace': 'https://id.namespace', 'author': 'author', 'role': 'role', 'timestamp': '2022-12-15T17:10:35.513000+01:00', 'last_updated': '2022-12-16T17:13:18.282000+01:00', 'user': 4, 'product': 1}, {'id': 2, 'product_data': None, 'vulnerability_names': 'CVE_vulnerability', 'branch_names': 'db_branch_internal_main', 'user_full_name': 'db_external', 'document_id_prefix': 'openvex_prefix', 'document_base_id': '2024_0002', 'version': 1, 'content_hash': 'abcdef123456', 'id_namespace': 'https://id.namespace', 'author': 'author', 'role': 'role', 'timestamp': '2022-12-15T17:10:35.513000+01:00', 'last_updated': '2022-12-16T17:13:18.282000+01:00', 'user': 4, 'product': None}]}"
        self._test_api(
            APITest("db_admin", "get", "/api/vex/openvex/", None, 200, expected_data)
        )

        expected_data = "{'count': 1, 'next': None, 'previous': None, 'results': [{'id': 1, 'product_data': {'id': 1, 'permissions': {<Permissions.VEX_View: 5001>, <Permissions.VEX_Edit: 5002>, <Permissions.VEX_Delete: 5003>, <Permissions.VEX_Create: 5004>, <Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Observation_Log_Approval: 2101>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_Authorization_Group_Member_View: 1601>, <Permissions.Product_Authorization_Group_Member_Edit: 1602>, <Permissions.Product_Authorization_Group_Member_Delete: 1603>, <Permissions.Product_Authorization_Group_Member_Create: 1604>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Service_View: 1501>, <Permissions.Service_Delete: 1503>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}, 'product_group_assessments_need_approval': False, 'name': 'db_product_internal', 'description': '', 'purl': '', 'cpe23': '', 'repository_prefix': '', 'repository_branch_housekeeping_active': None, 'repository_branch_housekeeping_keep_inactive_days': None, 'repository_branch_housekeeping_exempt_branches': '', 'security_gate_passed': True, 'security_gate_active': None, 'security_gate_threshold_critical': None, 'security_gate_threshold_high': None, 'security_gate_threshold_medium': None, 'security_gate_threshold_low': None, 'security_gate_threshold_none': None, 'security_gate_threshold_unkown': None, 'apply_general_rules': True, 'notification_ms_teams_webhook': '', 'notification_slack_webhook': '', 'notification_email_to': '', 'issue_tracker_active': False, 'issue_tracker_type': '', 'issue_tracker_base_url': '', 'issue_tracker_username': '', 'issue_tracker_api_key': '', 'issue_tracker_project_id': '', 'issue_tracker_labels': '', 'issue_tracker_issue_type': '', 'issue_tracker_status_closed': '', 'issue_tracker_minimum_severity': '', 'last_observation_change': '2022-12-16T17:13:18.283000+01:00', 'assessments_need_approval': False, 'product_group': 3, 'repository_default_branch': 1}, 'vulnerability_names': 'CVE_vulnerability_1', 'branch_names': 'db_branch_internal_dev', 'user_full_name': 'db_external', 'document_id_prefix': 'openvex_prefix', 'document_base_id': '2024_0001', 'version': 1, 'content_hash': 'abcdef123456', 'id_namespace': 'https://id.namespace', 'author': 'author', 'role': 'role', 'timestamp': '2022-12-15T17:10:35.513000+01:00', 'last_updated': '2022-12-16T17:13:18.282000+01:00', 'user': 4, 'product': 1}]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/vex/openvex/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'id': 1, 'product_data': {'id': 1, 'permissions': {<Permissions.VEX_View: 5001>, <Permissions.VEX_Edit: 5002>, <Permissions.VEX_Delete: 5003>, <Permissions.VEX_Create: 5004>, <Permissions.Product_Rule_View: 1301>, <Permissions.Product_Rule_Edit: 1302>, <Permissions.Product_Rule_Delete: 1303>, <Permissions.Product_Rule_Create: 1304>, <Permissions.Product_Rule_Apply: 1305>, <Permissions.Product_Api_Token_Revoke: 4003>, <Permissions.Product_Api_Token_Create: 4004>, <Permissions.Product_Member_View: 1201>, <Permissions.Product_Member_Edit: 1202>, <Permissions.Product_Member_Delete: 1203>, <Permissions.Product_Member_Create: 1204>, <Permissions.Observation_Log_Approval: 2101>, <Permissions.Api_Configuration_View: 3001>, <Permissions.Api_Configuration_Edit: 3002>, <Permissions.Api_Configuration_Delete: 3003>, <Permissions.Api_Configuration_Create: 3004>, <Permissions.Product_Authorization_Group_Member_View: 1601>, <Permissions.Product_Authorization_Group_Member_Edit: 1602>, <Permissions.Product_Authorization_Group_Member_Delete: 1603>, <Permissions.Product_Authorization_Group_Member_Create: 1604>, <Permissions.Product_View: 1101>, <Permissions.Product_Edit: 1102>, <Permissions.Product_Delete: 1103>, <Permissions.Product_Import_Observations: 1105>, <Permissions.Observation_View: 2001>, <Permissions.Observation_Edit: 2002>, <Permissions.Observation_Create: 2004>, <Permissions.Observation_Delete: 2003>, <Permissions.Observation_Assessment: 2005>, <Permissions.Service_View: 1501>, <Permissions.Service_Delete: 1503>, <Permissions.Product_Group_View: 1001>, <Permissions.Product_Group_Edit: 1002>, <Permissions.Product_Group_Delete: 1003>, <Permissions.Branch_View: 1401>, <Permissions.Branch_Edit: 1402>, <Permissions.Branch_Delete: 1403>, <Permissions.Branch_Create: 1404>}, 'product_group_assessments_need_approval': False, 'name': 'db_product_internal', 'description': '', 'purl': '', 'cpe23': '', 'repository_prefix': '', 'repository_branch_housekeeping_active': None, 'repository_branch_housekeeping_keep_inactive_days': None, 'repository_branch_housekeeping_exempt_branches': '', 'security_gate_passed': True, 'security_gate_active': None, 'security_gate_threshold_critical': None, 'security_gate_threshold_high': None, 'security_gate_threshold_medium': None, 'security_gate_threshold_low': None, 'security_gate_threshold_none': None, 'security_gate_threshold_unkown': None, 'apply_general_rules': True, 'notification_ms_teams_webhook': '', 'notification_slack_webhook': '', 'notification_email_to': '', 'issue_tracker_active': False, 'issue_tracker_type': '', 'issue_tracker_base_url': '', 'issue_tracker_username': '', 'issue_tracker_api_key': '', 'issue_tracker_project_id': '', 'issue_tracker_labels': '', 'issue_tracker_issue_type': '', 'issue_tracker_status_closed': '', 'issue_tracker_minimum_severity': '', 'last_observation_change': '2022-12-16T17:13:18.283000+01:00', 'assessments_need_approval': False, 'product_group': 3, 'repository_default_branch': 1}, 'vulnerability_names': 'CVE_vulnerability_1', 'branch_names': 'db_branch_internal_dev', 'user_full_name': 'db_external', 'document_id_prefix': 'openvex_prefix', 'document_base_id': '2024_0001', 'version': 1, 'content_hash': 'abcdef123456', 'id_namespace': 'https://id.namespace', 'author': 'author', 'role': 'role', 'timestamp': '2022-12-15T17:10:35.513000+01:00', 'last_updated': '2022-12-16T17:13:18.282000+01:00', 'user': 4, 'product': 1}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/vex/openvex/1/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'message': 'No OpenVEX matches the given query.'}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/vex/openvex/2/",
                None,
                404,
                expected_data,
            )
        )

        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/vex/openvex/99999/",
                None,
                404,
                expected_data,
            )
        )

        expected_data = "{'count': 1, 'next': None, 'previous': None, 'results': [{'id': 1, 'name': 'db_branch_internal_dev', 'openvex': 1, 'branch': 1}]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/vex/openvex_branches/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = (
            "{'id': 1, 'name': 'db_branch_internal_dev', 'openvex': 1, 'branch': 1}"
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/vex/openvex_branches/1/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'count': 1, 'next': None, 'previous': None, 'results': [{'id': 2, 'name': 'CVE_vulnerability_1', 'openvex': 1}]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/vex/openvex_vulnerabilities/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = (
            "{'message': 'No OpenVEX_Vulnerability matches the given query.'}"
        )
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/vex/openvex_vulnerabilities/1/",
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
                "db_internal_read",
                "delete",
                "/api/vex/openvex/1/",
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
                "/api/vex/openvex/1/",
                None,
                204,
                expected_data,
            )
        )


class TestAuthorizationOpenVEX_User(TestAuthorizationBase):
    def test_authorization_openvex(self):
        expected_data = "{'count': 1, 'next': None, 'previous': None, 'results': [{'id': 2, 'product_data': None, 'vulnerability_names': 'CVE_vulnerability', 'branch_names': 'db_branch_internal_main', 'user_full_name': 'db_external', 'document_id_prefix': 'openvex_prefix', 'document_base_id': '2024_0002', 'version': 1, 'content_hash': 'abcdef123456', 'id_namespace': 'https://id.namespace', 'author': 'author', 'role': 'role', 'timestamp': '2022-12-15T17:10:35.513000+01:00', 'last_updated': '2022-12-16T17:13:18.282000+01:00', 'user': 4, 'product': None}]}"
        self._test_api(
            APITest("db_external", "get", "/api/vex/openvex/", None, 200, expected_data)
        )

        expected_data = "{'message': 'No OpenVEX matches the given query.'}"
        self._test_api(
            APITest(
                "db_external",
                "get",
                "/api/vex/openvex/1/",
                None,
                404,
                expected_data,
            )
        )

        expected_data = "{'id': 2, 'product_data': None, 'vulnerability_names': 'CVE_vulnerability', 'branch_names': 'db_branch_internal_main', 'user_full_name': 'db_external', 'document_id_prefix': 'openvex_prefix', 'document_base_id': '2024_0002', 'version': 1, 'content_hash': 'abcdef123456', 'id_namespace': 'https://id.namespace', 'author': 'author', 'role': 'role', 'timestamp': '2022-12-15T17:10:35.513000+01:00', 'last_updated': '2022-12-16T17:13:18.282000+01:00', 'user': 4, 'product': None}"
        self._test_api(
            APITest(
                "db_external",
                "get",
                "/api/vex/openvex/2/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'message': 'No OpenVEX matches the given query.'}"
        self._test_api(
            APITest(
                "db_external",
                "get",
                "/api/vex/openvex/99999/",
                None,
                404,
                expected_data,
            )
        )

        expected_data = "{'count': 1, 'next': None, 'previous': None, 'results': [{'id': 2, 'name': 'db_branch_internal_main', 'openvex': 2, 'branch': 2}]}"
        self._test_api(
            APITest(
                "db_external",
                "get",
                "/api/vex/openvex_branches/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'message': 'No OpenVEX_Branch matches the given query.'}"
        self._test_api(
            APITest(
                "db_external",
                "get",
                "/api/vex/openvex_branches/1/",
                None,
                404,
                expected_data,
            )
        )

        expected_data = "{'count': 1, 'next': None, 'previous': None, 'results': [{'id': 1, 'name': 'CVE_vulnerability', 'openvex': 2}]}"
        self._test_api(
            APITest(
                "db_external",
                "get",
                "/api/vex/openvex_vulnerabilities/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'id': 1, 'name': 'CVE_vulnerability', 'openvex': 2}"
        self._test_api(
            APITest(
                "db_external",
                "get",
                "/api/vex/openvex_vulnerabilities/1/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "None"
        self._test_api(
            APITest(
                "db_external",
                "delete",
                "/api/vex/openvex/2/",
                None,
                204,
                expected_data,
            )
        )
