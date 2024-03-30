from django.core.management import call_command

from application.core.models import Observation
from unittests.access_control.api.test_authorization import (
    APITest,
    TestAuthorizationBase,
)


class TestAuthorizationPotentialDuplicates(TestAuthorizationBase):
    def test_authorization_potential_duplicates_product_member(self):
        self._test_authorization_potential_duplicates()

    def test_authorization_potential_duplicates_product_authorization_group_member(
        self,
    ):
        self._prepare_authorization_groups()
        self._test_authorization_potential_duplicates()

    def _test_authorization_potential_duplicates(self):
        expected_data = "{'count': 2, 'next': None, 'previous': None, 'results': [{'id': 1, 'potential_duplicate_observation': {'id': 1, 'scanner_name': 'db_parser', 'origin_component_name_version': '', 'title': 'db_observation_internal', 'description': '', 'recommendation': '', 'current_severity': 'Medium', 'parser_severity': 'Medium', 'rule_severity': '', 'assessment_severity': '', 'current_status': 'Duplicate', 'parser_status': 'Open', 'rule_status': 'Duplicate', 'assessment_status': '', 'scanner_observation_id': '', 'vulnerability_id': '', 'origin_component_name': '', 'origin_component_version': '', 'origin_component_purl': '', 'origin_component_cpe': '', 'origin_component_dependencies': '', 'origin_docker_image_name': '', 'origin_docker_image_tag': '', 'origin_docker_image_name_tag': '', 'origin_docker_image_name_tag_short': '', 'origin_docker_image_digest': '', 'origin_endpoint_url': '', 'origin_endpoint_scheme': '', 'origin_endpoint_hostname': '', 'origin_endpoint_port': None, 'origin_endpoint_path': '', 'origin_endpoint_params': '', 'origin_endpoint_query': '', 'origin_endpoint_fragment': '', 'origin_service_name': 'db_service_internal_backend', 'origin_source_file': '', 'origin_source_line_start': None, 'origin_source_line_end': None, 'origin_cloud_provider': '', 'origin_cloud_account_subscription_project': '', 'origin_cloud_resource': '', 'origin_cloud_resource_type': '', 'origin_cloud_qualified_resource': '', 'cvss3_score': None, 'cvss3_vector': '', 'cwe': None, 'epss_score': None, 'epss_percentile': None, 'found': None, 'scanner': 'db_parser', 'upload_filename': 'parser.json', 'api_configuration_name': '', 'import_last_seen': '2022-12-15T17:14:20.870000+01:00', 'created': '2022-12-15T17:10:35.513000+01:00', 'modified': '2022-12-16T17:13:18.282000+01:00', 'last_observation_log': '2022-12-16T17:13:18.281000+01:00', 'identity_hash': '6eef8088480aa2523aeeb64ad35f876a942cc3172cfb36752f3a052a4f88642c', 'issue_tracker_issue_id': '', 'issue_tracker_issue_closed': False, 'has_potential_duplicates': False, 'current_vex_justification': '', 'parser_vex_justification': '', 'rule_vex_justification': '', 'assessment_vex_justification': '', 'product': 1, 'branch': 1, 'parser': 1, 'origin_service': 1, 'general_rule': None, 'product_rule': 1}, 'type': 'Component', 'observation': 1}, {'id': 2, 'potential_duplicate_observation': {'id': 2, 'scanner_name': 'db_parser', 'origin_component_name_version': '', 'title': 'db_observation_internal', 'description': '', 'recommendation': '', 'current_severity': 'Medium', 'parser_severity': 'Medium', 'rule_severity': '', 'assessment_severity': '', 'current_status': 'False positive', 'parser_status': 'Open', 'rule_status': 'False positive', 'assessment_status': '', 'scanner_observation_id': '', 'vulnerability_id': '', 'origin_component_name': '', 'origin_component_version': '', 'origin_component_purl': '', 'origin_component_cpe': '', 'origin_component_dependencies': '', 'origin_docker_image_name': '', 'origin_docker_image_tag': '', 'origin_docker_image_name_tag': '', 'origin_docker_image_name_tag_short': '', 'origin_docker_image_digest': '', 'origin_endpoint_url': '', 'origin_endpoint_scheme': '', 'origin_endpoint_hostname': '', 'origin_endpoint_port': None, 'origin_endpoint_path': '', 'origin_endpoint_params': '', 'origin_endpoint_query': '', 'origin_endpoint_fragment': '', 'origin_service_name': '', 'origin_source_file': '', 'origin_source_line_start': None, 'origin_source_line_end': None, 'origin_cloud_provider': '', 'origin_cloud_account_subscription_project': '', 'origin_cloud_resource': '', 'origin_cloud_resource_type': '', 'origin_cloud_qualified_resource': '', 'cvss3_score': None, 'cvss3_vector': '', 'cwe': None, 'epss_score': None, 'epss_percentile': None, 'found': None, 'scanner': 'db_parser', 'upload_filename': 'parser.json', 'api_configuration_name': '', 'import_last_seen': '2022-12-15T17:14:20.876000+01:00', 'created': '2022-12-15T17:10:35.521000+01:00', 'modified': '2022-12-16T17:13:18.283000+01:00', 'last_observation_log': '2022-12-16T17:13:18.283000+01:00', 'identity_hash': 'bc8e59b7687fe3533616b3914c636389c131eac3bdbda1b67d8d26f890a74007', 'issue_tracker_issue_id': '', 'issue_tracker_issue_closed': False, 'has_potential_duplicates': False, 'current_vex_justification': '', 'parser_vex_justification': '', 'rule_vex_justification': '', 'assessment_vex_justification': '', 'product': 2, 'branch': None, 'parser': 1, 'origin_service': None, 'general_rule': None, 'product_rule': 2}, 'type': 'Source', 'observation': 2}]}"
        self._test_api(
            APITest(
                "db_admin",
                "get",
                "/api/potential_duplicates/",
                None,
                200,
                expected_data,
            )
        )

        expected_data = "{'count': 1, 'next': None, 'previous': None, 'results': [{'id': 1, 'potential_duplicate_observation': {'id': 1, 'scanner_name': 'db_parser', 'origin_component_name_version': '', 'title': 'db_observation_internal', 'description': '', 'recommendation': '', 'current_severity': 'Medium', 'parser_severity': 'Medium', 'rule_severity': '', 'assessment_severity': '', 'current_status': 'Duplicate', 'parser_status': 'Open', 'rule_status': 'Duplicate', 'assessment_status': '', 'scanner_observation_id': '', 'vulnerability_id': '', 'origin_component_name': '', 'origin_component_version': '', 'origin_component_purl': '', 'origin_component_cpe': '', 'origin_component_dependencies': '', 'origin_docker_image_name': '', 'origin_docker_image_tag': '', 'origin_docker_image_name_tag': '', 'origin_docker_image_name_tag_short': '', 'origin_docker_image_digest': '', 'origin_endpoint_url': '', 'origin_endpoint_scheme': '', 'origin_endpoint_hostname': '', 'origin_endpoint_port': None, 'origin_endpoint_path': '', 'origin_endpoint_params': '', 'origin_endpoint_query': '', 'origin_endpoint_fragment': '', 'origin_service_name': 'db_service_internal_backend', 'origin_source_file': '', 'origin_source_line_start': None, 'origin_source_line_end': None, 'origin_cloud_provider': '', 'origin_cloud_account_subscription_project': '', 'origin_cloud_resource': '', 'origin_cloud_resource_type': '', 'origin_cloud_qualified_resource': '', 'cvss3_score': None, 'cvss3_vector': '', 'cwe': None, 'epss_score': None, 'epss_percentile': None, 'found': None, 'scanner': 'db_parser', 'upload_filename': 'parser.json', 'api_configuration_name': '', 'import_last_seen': '2022-12-15T17:14:20.870000+01:00', 'created': '2022-12-15T17:10:35.513000+01:00', 'modified': '2022-12-16T17:13:18.282000+01:00', 'last_observation_log': '2022-12-16T17:13:18.281000+01:00', 'identity_hash': '6eef8088480aa2523aeeb64ad35f876a942cc3172cfb36752f3a052a4f88642c', 'issue_tracker_issue_id': '', 'issue_tracker_issue_closed': False, 'has_potential_duplicates': False, 'current_vex_justification': '', 'parser_vex_justification': '', 'rule_vex_justification': '', 'assessment_vex_justification': '', 'product': 1, 'branch': 1, 'parser': 1, 'origin_service': 1, 'general_rule': None, 'product_rule': 1}, 'type': 'Component', 'observation': 1}]}"
        self._test_api(
            APITest(
                "db_internal_write",
                "get",
                "/api/potential_duplicates/",
                None,
                200,
                expected_data,
            )
        )
