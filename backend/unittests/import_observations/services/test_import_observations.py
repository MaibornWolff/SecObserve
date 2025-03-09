from unittest.mock import call, patch

from django.core.files.base import File
from django.core.management import call_command

from application.access_control.models import User
from application.commons.models import Settings
from application.core.models import (
    Branch,
    Evidence,
    Observation,
    Observation_Log,
    Product,
    Reference,
)
from application.core.types import Severity, Status
from application.import_observations.models import Vulnerability_Check
from application.import_observations.services.import_observations import (
    FileUploadParameters,
    file_upload_observations,
)
from application.licenses.models import (
    License,
    License_Component,
    License_Policy,
    License_Policy_Item,
)
from application.licenses.types import License_Policy_Evaluation_Result
from application.rules.models import Rule
from unittests.base_test_case import BaseTestCase


class TestImportObservations(BaseTestCase):
    def setUp(self):
        Observation.objects.all().delete()
        Observation_Log.objects.all().delete()
        Rule.objects.all().delete()
        Vulnerability_Check.objects.all().delete()
        call_command("loaddata", "unittests/fixtures/import_observations_fixtures.json")
        super().setUp()

    @patch("application.commons.services.global_request.get_current_request")
    @patch("application.import_observations.services.import_observations.check_security_gate")
    @patch("application.import_observations.services.import_observations.set_repository_default_branch")
    @patch("application.import_observations.services.import_observations.push_observations_to_issue_tracker")
    @patch("application.import_observations.services.import_observations.apply_epss")
    @patch("application.import_observations.services.import_observations.apply_exploit_information")
    @patch("application.import_observations.services.import_observations.find_potential_duplicates")
    @patch("application.vex.services.vex_engine.VEX_Engine.apply_vex_statements_for_observation")
    def test_file_upload_observations_with_branch(
        self,
        mock_apply_vex_statements_for_observation,
        mock_find_potential_duplicates,
        mock_apply_exploit_information,
        mock_apply_epss,
        mock_push_observations_to_issue_tracker,
        mock_set_repository_default_branch,
        mock_check_security_gate,
        mock_get_current_request,
    ):
        mock_get_current_request.return_value = RequestMock(User.objects.get(id=1))

        self._file_upload_observations(
            Branch.objects.get(id=1),
            "test_service",
            "test_docker_image_name_tag",
            "test_endpoint_url",
            "test_kubernetes_cluster",
        )

        product = Product.objects.get(id=1)
        mock_check_security_gate.assert_has_calls([call(product), call(product)])
        mock_set_repository_default_branch.assert_has_calls([call(product), call(product)])
        self.assertEqual(mock_push_observations_to_issue_tracker.call_count, 2)
        self.assertEqual(mock_apply_epss.call_count, 4)
        self.assertEqual(mock_apply_exploit_information.call_count, 4)
        self.assertEqual(mock_find_potential_duplicates.call_count, 2)
        self.assertEqual(mock_apply_vex_statements_for_observation.call_count, 4)

    @patch("application.commons.services.global_request.get_current_request")
    @patch("application.import_observations.services.import_observations.check_security_gate")
    @patch("application.import_observations.services.import_observations.set_repository_default_branch")
    @patch("application.import_observations.services.import_observations.push_observations_to_issue_tracker")
    @patch("application.import_observations.services.import_observations.apply_epss")
    @patch("application.import_observations.services.import_observations.apply_exploit_information")
    @patch("application.import_observations.services.import_observations.find_potential_duplicates")
    @patch("application.vex.services.vex_engine.VEX_Engine.apply_vex_statements_for_observation")
    def test_file_upload_observations_without_branch(
        self,
        mock_apply_vex_statements_for_observation,
        mock_find_potential_duplicates,
        mock_apply_exploit_information,
        mock_apply_epss,
        mock_push_observations_to_issue_tracker,
        mock_set_repository_default_branch,
        mock_check_security_gate,
        mock_get_current_request,
    ):
        mock_get_current_request.return_value = RequestMock(User.objects.get(id=1))
        self._file_upload_observations(None, None, None, None, None)

        product = Product.objects.get(id=1)
        mock_check_security_gate.assert_has_calls([call(product), call(product)])
        mock_set_repository_default_branch.assert_has_calls([call(product), call(product)])
        self.assertEqual(mock_push_observations_to_issue_tracker.call_count, 2)
        self.assertEqual(mock_apply_epss.call_count, 4)
        self.assertEqual(mock_apply_exploit_information.call_count, 4)
        self.assertEqual(mock_find_potential_duplicates.call_count, 2)
        self.assertEqual(mock_apply_vex_statements_for_observation.call_count, 4)

    def _file_upload_observations(self, branch, service, docker_image_name_tag, endpoint_url, kubernetes_cluster):
        # --- First import ---

        file_upload_parameters = FileUploadParameters(
            product=Product.objects.get(id=1),
            branch=branch,
            file=File(open("unittests/fixtures/data_1/bandit.sarif", "r")),
            service=service,
            docker_image_name_tag=docker_image_name_tag,
            endpoint_url=endpoint_url,
            kubernetes_cluster=kubernetes_cluster,
            suppress_licenses=False,
        )

        (
            new_observations,
            updated_observations,
            resolved_observations,
            new_license_objects,
            updated_license_objects,
            deleted_license_objects,
        ) = file_upload_observations(file_upload_parameters)

        self.assertEqual(new_observations, 2)
        self.assertEqual(updated_observations, 0)
        self.assertEqual(resolved_observations, 0)
        self.assertEqual(new_license_objects, 0)
        self.assertEqual(updated_license_objects, 0)
        self.assertEqual(deleted_license_objects, 0)

        product = Product.objects.get(id=1)

        observations = Observation.objects.filter(product=1).order_by("id")
        self.assertEqual(len(observations), 3)

        self.assertEqual(observations[0].product, product)
        self.assertEqual(observations[0].branch, branch)
        if service:
            self.assertEqual(observations[0].origin_service_name, service)
        else:
            self.assertEqual(observations[0].origin_service_name, "")
        if docker_image_name_tag:
            self.assertEqual(observations[0].origin_docker_image_name_tag, docker_image_name_tag)
        else:
            self.assertEqual(observations[0].origin_docker_image_name_tag, "")
        if endpoint_url:
            self.assertEqual(observations[0].origin_endpoint_url, endpoint_url)
        else:
            self.assertEqual(observations[0].origin_endpoint_url, "")
        if kubernetes_cluster:
            self.assertEqual(observations[0].origin_kubernetes_cluster, kubernetes_cluster)
        else:
            self.assertEqual(observations[0].origin_kubernetes_cluster, "")

        self.assertEqual(observations[0].current_status, Status.STATUS_OPEN)
        self.assertEqual(observations[1].current_status, Status.STATUS_OPEN)
        self.assertEqual(observations[2].current_status, Status.STATUS_NOT_AFFECTED)

        observation_logs = Observation_Log.objects.filter(observation__product=1).order_by("id")
        self.assertEqual(len(observation_logs), 4)

        self.assertEqual(observation_logs[0].observation, observations[0])
        self.assertEqual(observation_logs[1].observation, observations[1])

        self.assertEqual(observation_logs[2].observation, observations[2])
        self.assertEqual(observation_logs[2].severity, observations[2].current_severity)
        self.assertEqual(observation_logs[2].status, Status.STATUS_OPEN)
        self.assertEqual(observation_logs[2].comment, "Set by parser")

        self.assertEqual(observation_logs[3].observation, observations[2])
        self.assertEqual(observation_logs[3].severity, "")
        self.assertEqual(observation_logs[3].status, observations[2].current_status)
        self.assertEqual(
            observation_logs[3].comment,
            "Updated by product rule db_product_rule_import",
        )

        references = Reference.objects.filter(observation__product=product).order_by("id")
        self.assertEqual(len(references), 3)

        self.assertEqual(references[0].observation, observations[0])
        self.assertEqual(
            references[0].url,
            "https://bandit.readthedocs.io/en/1.7.4/plugins/b104_hardcoded_bind_all_interfaces.html",
        )

        evidences = Evidence.objects.filter(observation__product=product).order_by("id")
        self.assertEqual(len(evidences), 6)

        vulnerability_checks = Vulnerability_Check.objects.filter(product=1)
        self.assertEqual(len(vulnerability_checks), 1)

        self.assertEqual(vulnerability_checks[0].product, product)
        self.assertEqual(vulnerability_checks[0].branch, branch)
        self.assertEqual(vulnerability_checks[0].filename, "bandit.sarif")
        self.assertEqual(vulnerability_checks[0].api_configuration_name, "")
        self.assertEqual(vulnerability_checks[0].scanner, "Bandit")
        self.assertEqual(vulnerability_checks[0].last_import_observations_new, 2)
        self.assertEqual(vulnerability_checks[0].last_import_observations_updated, 0)
        self.assertEqual(vulnerability_checks[0].last_import_observations_resolved, 0)

        # --- Second import with some changes ---

        file_upload_parameters = FileUploadParameters(
            product=Product.objects.get(id=1),
            branch=branch,
            file=File(open("unittests/fixtures/data_2/bandit.sarif", "r")),
            service=service,
            docker_image_name_tag=docker_image_name_tag,
            endpoint_url=endpoint_url,
            kubernetes_cluster=kubernetes_cluster,
            suppress_licenses=False,
        )

        (
            new_observations,
            updated_observations,
            resolved_observations,
            new_license_objects,
            updated_license_objects,
            deleted_license_objects,
        ) = file_upload_observations(file_upload_parameters)

        self.assertEqual(new_observations, 0)
        self.assertEqual(updated_observations, 1)
        self.assertEqual(resolved_observations, 1)
        self.assertEqual(new_license_objects, 0)
        self.assertEqual(updated_license_objects, 0)
        self.assertEqual(deleted_license_objects, 0)

        observations = Observation.objects.filter(product=1).order_by("id")
        self.assertEqual(len(observations), 3)

        self.assertEqual(observations[0].current_status, Status.STATUS_RESOLVED)
        self.assertEqual(observations[1].current_status, Status.STATUS_OPEN)
        self.assertEqual(observations[2].current_status, Status.STATUS_RESOLVED)

        observation_logs = Observation_Log.objects.filter(observation__product=1).order_by("id")
        self.assertEqual(len(observation_logs), 7)

        self.assertEqual(observation_logs[4].observation, observations[1])
        self.assertEqual(observation_logs[4].severity, Severity.SEVERITY_HIGH)
        self.assertEqual(observation_logs[4].status, "")
        self.assertEqual(observation_logs[4].comment, "Updated by parser")

        self.assertEqual(observation_logs[5].observation, observations[0])
        self.assertEqual(observation_logs[5].severity, "")
        self.assertEqual(observation_logs[5].status, Status.STATUS_RESOLVED)
        self.assertEqual(observation_logs[5].comment, "Observation not found in latest scan")

        self.assertEqual(observation_logs[6].observation, observations[2])
        self.assertEqual(observation_logs[6].severity, "")
        self.assertEqual(observation_logs[6].status, Status.STATUS_RESOLVED)
        self.assertEqual(observation_logs[6].comment, "Observation not found in latest scan")

        references = Reference.objects.filter(observation__product=product).order_by("id")
        self.assertEqual(len(references), 3)

        evidences = Evidence.objects.filter(observation__product=product).order_by("id")
        self.assertEqual(len(evidences), 6)

        vulnerability_checks = Vulnerability_Check.objects.filter(product=1)
        self.assertEqual(len(vulnerability_checks), 1)

        self.assertEqual(vulnerability_checks[0].product, product)
        self.assertEqual(vulnerability_checks[0].branch, branch)
        self.assertEqual(vulnerability_checks[0].filename, "bandit.sarif")
        self.assertEqual(vulnerability_checks[0].api_configuration_name, "")
        self.assertEqual(vulnerability_checks[0].scanner, "Bandit")
        self.assertEqual(vulnerability_checks[0].last_import_observations_new, 0)
        self.assertEqual(vulnerability_checks[0].last_import_observations_updated, 1)
        self.assertEqual(vulnerability_checks[0].last_import_observations_resolved, 1)

    @patch("application.commons.services.global_request.get_current_request")
    @patch("application.import_observations.services.import_observations.check_security_gate")
    @patch("application.import_observations.services.import_observations.set_repository_default_branch")
    @patch("application.import_observations.services.import_observations.push_observations_to_issue_tracker")
    @patch("application.import_observations.services.import_observations.apply_epss")
    @patch("application.import_observations.services.import_observations.apply_exploit_information")
    @patch("application.import_observations.services.import_observations.find_potential_duplicates")
    @patch("application.vex.services.vex_engine.VEX_Engine.apply_vex_statements_for_observation")
    @patch("application.import_observations.parsers.cyclone_dx.parser.CycloneDXParser.get_license_components")
    @patch("application.import_observations.services.import_observations.process_license_components")
    def test_file_upload_licenses_feature_false(
        self,
        mock_process_license_components,
        mock_get_license_components,
        mock_apply_vex_statements_for_observation,
        mock_find_potential_duplicates,
        mock_apply_exploit_information,
        mock_apply_epss,
        mock_push_observations_to_issue_tracker,
        mock_set_repository_default_branch,
        mock_check_security_gate,
        mock_get_current_request,
    ):
        mock_get_current_request.return_value = RequestMock(User.objects.get(id=1))

        settings = Settings.load()
        settings.feature_license_management = False
        settings.save()

        self._file_upload_licenses(
            Branch.objects.get(id=1),
            "test_service",
            "test_docker_image_name_tag",
            "test_endpoint_url",
            "test_kubernetes_cluster",
            suppress_licenses=False,
        )

        self.assertEqual(mock_get_license_components.call_count, 0)
        self.assertEqual(mock_process_license_components.call_count, 0)

        settings = Settings.load()
        settings.feature_license_management = True
        settings.save()

    @patch("application.commons.services.global_request.get_current_request")
    @patch("application.import_observations.services.import_observations.check_security_gate")
    @patch("application.import_observations.services.import_observations.set_repository_default_branch")
    @patch("application.import_observations.services.import_observations.push_observations_to_issue_tracker")
    @patch("application.import_observations.services.import_observations.apply_epss")
    @patch("application.import_observations.services.import_observations.apply_exploit_information")
    @patch("application.import_observations.services.import_observations.find_potential_duplicates")
    @patch("application.vex.services.vex_engine.VEX_Engine.apply_vex_statements_for_observation")
    @patch("application.import_observations.parsers.cyclone_dx.parser.CycloneDXParser.get_license_components")
    @patch("application.import_observations.services.import_observations.process_license_components")
    def test_file_upload_suppress_licenses_true(
        self,
        mock_process_license_components,
        mock_get_license_components,
        mock_apply_vex_statements_for_observation,
        mock_find_potential_duplicates,
        mock_apply_exploit_information,
        mock_apply_epss,
        mock_push_observations_to_issue_tracker,
        mock_set_repository_default_branch,
        mock_check_security_gate,
        mock_get_current_request,
    ):
        mock_get_current_request.return_value = RequestMock(User.objects.get(id=1))

        self._file_upload_licenses(
            Branch.objects.get(id=1),
            "test_service",
            "test_docker_image_name_tag",
            "test_endpoint_url",
            "test_kubernetes_cluster",
            suppress_licenses=True,
        )

        self.assertEqual(mock_get_license_components.call_count, 0)
        self.assertEqual(mock_process_license_components.call_count, 0)

    @patch("application.commons.services.global_request.get_current_request")
    @patch("application.import_observations.services.import_observations.check_security_gate")
    @patch("application.import_observations.services.import_observations.set_repository_default_branch")
    @patch("application.import_observations.services.import_observations.push_observations_to_issue_tracker")
    @patch("application.import_observations.services.import_observations.apply_epss")
    @patch("application.import_observations.services.import_observations.apply_exploit_information")
    @patch("application.import_observations.services.import_observations.find_potential_duplicates")
    @patch("application.vex.services.vex_engine.VEX_Engine.apply_vex_statements_for_observation")
    def test_file_upload_licenses_feature_true(
        self,
        mock_apply_vex_statements_for_observation,
        mock_find_potential_duplicates,
        mock_apply_exploit_information,
        mock_apply_epss,
        mock_push_observations_to_issue_tracker,
        mock_set_repository_default_branch,
        mock_check_security_gate,
        mock_get_current_request,
    ):
        mock_get_current_request.return_value = RequestMock(User.objects.get(id=1))

        settings = Settings.load()
        settings.feature_license_management = True
        settings.save()

        self._file_upload_licenses(
            Branch.objects.get(id=1),
            "test_service",
            "test_docker_image_name_tag",
            "test_endpoint_url",
            "test_kubernetes_cluster",
            suppress_licenses=False,
        )

    def _file_upload_licenses(
        self,
        branch,
        service,
        docker_image_name_tag,
        endpoint_url,
        kubernetes_cluster,
        suppress_licenses,
    ):
        License_Component.objects.all().delete()

        # --- First import without license policy ---

        file_upload_parameters = FileUploadParameters(
            product=Product.objects.get(id=1),
            branch=branch,
            file=File(
                open(
                    "unittests/import_observations/parsers/cyclone_dx/files/licenses_1.json",
                    "r",
                )
            ),
            service=service,
            docker_image_name_tag=docker_image_name_tag,
            endpoint_url=endpoint_url,
            kubernetes_cluster=kubernetes_cluster,
            suppress_licenses=suppress_licenses,
        )

        (
            new_observations,
            updated_observations,
            resolved_observations,
            new_license_objects,
            updated_license_objects,
            deleted_license_objects,
        ) = file_upload_observations(file_upload_parameters)

        settings = Settings.load()
        if settings.feature_license_management and not suppress_licenses:
            self.assertEqual(new_observations, 0)
            self.assertEqual(updated_observations, 0)
            self.assertEqual(resolved_observations, 0)
            self.assertEqual(new_license_objects, 67)
            self.assertEqual(updated_license_objects, 0)
            self.assertEqual(deleted_license_objects, 0)

            license_components = License_Component.objects.filter(product=1).order_by("id")
            self.assertEqual(len(license_components), 67)

            self.assertEqual(license_components[1].branch, branch)
            self.assertEqual(license_components[1].upload_filename, "licenses_1.json")
            self.assertEqual(license_components[1].component_name, "argon2-cffi-bindings")
            self.assertEqual(license_components[1].component_version, "21.2.0")
            self.assertEqual(
                license_components[1].component_name_version,
                "argon2-cffi-bindings:21.2.0",
            )
            self.assertEqual(
                license_components[1].component_purl,
                "pkg:pypi/argon2-cffi-bindings@21.2.0",
            )
            self.assertEqual(license_components[1].component_purl_type, "pypi")
            self.assertEqual(license_components[1].component_cpe, "")
            dependencies = """SecObserve:1.28.2 --> argon2-cffi:23.1.0
argon2-cffi:23.1.0 --> argon2-cffi-bindings:21.2.0"""
            self.assertEqual(license_components[1].component_dependencies, dependencies)
            self.assertEqual(license_components[1].license, License.objects.get(spdx_id="MIT"))
            self.assertEqual(license_components[1].non_spdx_license, "")
            self.assertEqual(
                license_components[1].evaluation_result,
                License_Policy_Evaluation_Result.RESULT_UNKNOWN,
            )
            self.assertEqual(
                license_components[1].numerical_evaluation_result,
                License_Policy_Evaluation_Result.NUMERICAL_RESULTS.get(
                    License_Policy_Evaluation_Result.RESULT_UNKNOWN,
                ),
            )

            self.assertEqual(license_components[3].component_name_version, "asgiref:3.8.1")
            self.assertEqual(license_components[3].license, None)
            self.assertEqual(license_components[3].non_spdx_license, "0BSD, BSD-3-Clause")
            self.assertEqual(
                license_components[3].evaluation_result,
                License_Policy_Evaluation_Result.RESULT_UNKNOWN,
            )
            self.assertEqual(
                license_components[3].numerical_evaluation_result,
                License_Policy_Evaluation_Result.NUMERICAL_RESULTS.get(
                    License_Policy_Evaluation_Result.RESULT_UNKNOWN,
                ),
            )

            self.assertEqual(license_components[24].component_name_version, "email-validator:2.1.1")
            self.assertEqual(
                license_components[24].license_expression,
                "GPL-2.0-or-later WITH Bison-exception-2.2",
            )
            self.assertEqual(
                license_components[24].evaluation_result,
                License_Policy_Evaluation_Result.RESULT_UNKNOWN,
            )
            self.assertEqual(
                license_components[24].numerical_evaluation_result,
                License_Policy_Evaluation_Result.NUMERICAL_RESULTS.get(
                    License_Policy_Evaluation_Result.RESULT_UNKNOWN,
                ),
            )

        # --- Second import with license policy ---

        product = Product.objects.get(id=1)
        product.license_policy = License_Policy.objects.get(name="Standard")
        product.save()

        license_policy_item = License_Policy_Item(
            license_policy=License_Policy.objects.get(name="Standard"),
            license_group=None,
            license=None,
            license_expression="GPL-2.0-or-later WITH Bison-exception-2.2",
            non_spdx_license="",
            evaluation_result=License_Policy_Evaluation_Result.RESULT_FORBIDDEN,
        )
        license_policy_item.save()

        file_upload_parameters = FileUploadParameters(
            product=product,
            branch=branch,
            file=File(
                open(
                    "unittests/import_observations/parsers/cyclone_dx/files/licenses_1.json",
                    "r",
                )
            ),
            service=service,
            docker_image_name_tag=docker_image_name_tag,
            endpoint_url=endpoint_url,
            kubernetes_cluster=kubernetes_cluster,
            suppress_licenses=suppress_licenses,
        )

        (
            new_observations,
            updated_observations,
            resolved_observations,
            new_license_objects,
            updated_license_objects,
            deleted_license_objects,
        ) = file_upload_observations(file_upload_parameters)

        settings = Settings.load()
        if settings.feature_license_management and not suppress_licenses:
            self.assertEqual(new_observations, 0)
            self.assertEqual(updated_observations, 0)
            self.assertEqual(resolved_observations, 0)
            self.assertEqual(new_license_objects, 0)
            self.assertEqual(updated_license_objects, 67)
            self.assertEqual(deleted_license_objects, 0)

            license_components = License_Component.objects.filter(product=1).order_by("id")
            self.assertEqual(len(license_components), 67)

            self.assertEqual(
                license_components[1].component_name_version,
                "argon2-cffi-bindings:21.2.0",
            )
            self.assertEqual(license_components[1].license, License.objects.get(spdx_id="MIT"))
            self.assertEqual(license_components[1].non_spdx_license, "")
            self.assertEqual(
                license_components[1].evaluation_result,
                License_Policy_Evaluation_Result.RESULT_ALLOWED,
            )
            self.assertEqual(
                license_components[1].numerical_evaluation_result,
                License_Policy_Evaluation_Result.NUMERICAL_RESULTS.get(
                    License_Policy_Evaluation_Result.RESULT_ALLOWED,
                ),
            )

            self.assertEqual(license_components[3].component_name_version, "asgiref:3.8.1")
            self.assertEqual(license_components[3].license, None)
            self.assertEqual(license_components[3].non_spdx_license, "0BSD, BSD-3-Clause")
            self.assertEqual(
                license_components[3].evaluation_result,
                License_Policy_Evaluation_Result.RESULT_UNKNOWN,
            )
            self.assertEqual(
                license_components[3].numerical_evaluation_result,
                License_Policy_Evaluation_Result.NUMERICAL_RESULTS.get(
                    License_Policy_Evaluation_Result.RESULT_UNKNOWN,
                ),
            )

            self.assertEqual(license_components[9].component_name_version, "cryptography:43.0.1")
            self.assertEqual(license_components[9].license, None)
            self.assertEqual(
                license_components[9].license_expression,
                "LGPL-3.0-or-later OR BSD-3-Clause",
            )
            self.assertEqual(
                license_components[9].evaluation_result,
                License_Policy_Evaluation_Result.RESULT_ALLOWED,
            )
            self.assertEqual(
                license_components[9].numerical_evaluation_result,
                License_Policy_Evaluation_Result.NUMERICAL_RESULTS.get(
                    License_Policy_Evaluation_Result.RESULT_ALLOWED,
                ),
            )

            self.assertEqual(license_components[10].component_name_version, "cvss:3.2")
            self.assertEqual(license_components[10].license, None)
            self.assertEqual(
                license_components[10].license_expression,
                "GPL-3.0-or-later AND BSD-3-Clause",
            )
            self.assertEqual(
                license_components[10].evaluation_result,
                License_Policy_Evaluation_Result.RESULT_FORBIDDEN,
            )
            self.assertEqual(
                license_components[10].numerical_evaluation_result,
                License_Policy_Evaluation_Result.NUMERICAL_RESULTS.get(
                    License_Policy_Evaluation_Result.RESULT_FORBIDDEN,
                ),
            )

            self.assertEqual(license_components[11].component_name_version, "defusedcsv:2.0.0")
            self.assertEqual(license_components[11].license, None)
            self.assertEqual(
                license_components[11].license_expression,
                "(Apache-2.0 OR BSD-3-Clause) AND MIT",
            )
            self.assertEqual(
                license_components[11].evaluation_result,
                License_Policy_Evaluation_Result.RESULT_ALLOWED,
            )
            self.assertEqual(
                license_components[11].numerical_evaluation_result,
                License_Policy_Evaluation_Result.NUMERICAL_RESULTS.get(
                    License_Policy_Evaluation_Result.RESULT_ALLOWED,
                ),
            )

            self.assertEqual(license_components[24].component_name_version, "email-validator:2.1.1")
            self.assertEqual(
                license_components[24].license_expression,
                "GPL-2.0-or-later WITH Bison-exception-2.2",
            )
            self.assertEqual(
                license_components[24].evaluation_result,
                License_Policy_Evaluation_Result.RESULT_FORBIDDEN,
            )
            self.assertEqual(
                license_components[24].numerical_evaluation_result,
                License_Policy_Evaluation_Result.NUMERICAL_RESULTS.get(
                    License_Policy_Evaluation_Result.RESULT_FORBIDDEN,
                ),
            )

        # --- Third import with some changes ---

        license_policy = License_Policy.objects.get(name="Standard")
        license_policy.ignore_component_types = "npm"
        license_policy.save()

        license_policy_item = License_Policy_Item(
            license_policy=License_Policy.objects.get(name="Standard"),
            license_group=None,
            license=None,
            non_spdx_license="0BSD, BSD-3-Clause",
            evaluation_result=License_Policy_Evaluation_Result.RESULT_REVIEW_REQUIRED,
        )
        license_policy_item.save()
        license_policy_item = License_Policy_Item(
            license_policy=License_Policy.objects.get(name="Standard"),
            license_group=None,
            license=License.objects.get(spdx_id="MIT"),
            non_spdx_license="",
            evaluation_result=License_Policy_Evaluation_Result.RESULT_FORBIDDEN,
        )
        license_policy_item.save()

        license_policy_item.save()
        license_policy_item = License_Policy_Item(
            license_policy=License_Policy.objects.get(name="Standard"),
            license_group=None,
            license=License.objects.get(spdx_id="Apache-2.0"),
            non_spdx_license="",
            evaluation_result=License_Policy_Evaluation_Result.RESULT_FORBIDDEN,
        )
        license_policy_item.save()

        file_upload_parameters = FileUploadParameters(
            product=product,
            branch=branch,
            file=File(
                open(
                    "unittests/import_observations/parsers/cyclone_dx/files/changed/licenses_1.json",
                    "r",
                )
            ),
            service=service,
            docker_image_name_tag=docker_image_name_tag,
            endpoint_url=endpoint_url,
            kubernetes_cluster=kubernetes_cluster,
            suppress_licenses=suppress_licenses,
        )

        (
            new_observations,
            updated_observations,
            resolved_observations,
            new_license_objects,
            updated_license_objects,
            deleted_license_objects,
        ) = file_upload_observations(file_upload_parameters)

        settings = Settings.load()
        if settings.feature_license_management and not suppress_licenses:
            self.assertEqual(new_observations, 0)
            self.assertEqual(updated_observations, 0)
            self.assertEqual(resolved_observations, 0)
            self.assertEqual(new_license_objects, 3)
            self.assertEqual(updated_license_objects, 64)
            self.assertEqual(deleted_license_objects, 3)

            license_components = License_Component.objects.filter(product=1).order_by("id")
            self.assertEqual(len(license_components), 67)

            self.assertEqual(
                license_components[64].component_name_version,
                "argon2-cffi-bindings:21.2.1",
            )
            self.assertEqual(license_components[64].license, License.objects.get(spdx_id="MIT"))
            self.assertEqual(license_components[64].non_spdx_license, "")
            self.assertEqual(
                license_components[64].evaluation_result,
                License_Policy_Evaluation_Result.RESULT_FORBIDDEN,
            )
            self.assertEqual(
                license_components[64].numerical_evaluation_result,
                License_Policy_Evaluation_Result.NUMERICAL_RESULTS.get(
                    License_Policy_Evaluation_Result.RESULT_FORBIDDEN,
                ),
            )

            self.assertEqual(license_components[2].component_name_version, "asgiref:3.8.1")
            self.assertEqual(license_components[2].license, None)
            self.assertEqual(license_components[2].non_spdx_license, "0BSD, BSD-3-Clause")
            self.assertEqual(
                license_components[2].evaluation_result,
                License_Policy_Evaluation_Result.RESULT_REVIEW_REQUIRED,
            )
            self.assertEqual(
                license_components[2].numerical_evaluation_result,
                License_Policy_Evaluation_Result.NUMERICAL_RESULTS.get(
                    License_Policy_Evaluation_Result.RESULT_REVIEW_REQUIRED,
                ),
            )

            self.assertEqual(license_components[7].component_name_version, "cryptography:43.0.1")
            self.assertEqual(license_components[7].license, None)
            self.assertEqual(
                license_components[7].license_expression,
                "LGPL-3.0-or-later OR GPL-3.0-or-later",
            )
            self.assertEqual(
                license_components[7].evaluation_result,
                License_Policy_Evaluation_Result.RESULT_REVIEW_REQUIRED,
            )
            self.assertEqual(
                license_components[7].numerical_evaluation_result,
                License_Policy_Evaluation_Result.NUMERICAL_RESULTS.get(
                    License_Policy_Evaluation_Result.RESULT_REVIEW_REQUIRED,
                ),
            )

            self.assertEqual(license_components[8].component_name_version, "cvss:3.2")
            self.assertEqual(license_components[8].license, None)
            self.assertEqual(
                license_components[8].license_expression,
                "LGPL-3.0-or-later AND BSD-3-Clause",
            )
            self.assertEqual(
                license_components[8].evaluation_result,
                License_Policy_Evaluation_Result.RESULT_REVIEW_REQUIRED,
            )
            self.assertEqual(
                license_components[8].numerical_evaluation_result,
                License_Policy_Evaluation_Result.NUMERICAL_RESULTS.get(
                    License_Policy_Evaluation_Result.RESULT_REVIEW_REQUIRED,
                ),
            )

            self.assertEqual(license_components[9].component_name_version, "defusedcsv:2.0.0")
            self.assertEqual(license_components[9].license, None)
            self.assertEqual(
                license_components[9].license_expression,
                "Apache-2.0 AND (BSD-3-Clause OR MIT)",
            )
            self.assertEqual(
                license_components[9].evaluation_result,
                License_Policy_Evaluation_Result.RESULT_FORBIDDEN,
            )
            self.assertEqual(
                license_components[9].numerical_evaluation_result,
                License_Policy_Evaluation_Result.NUMERICAL_RESULTS.get(
                    License_Policy_Evaluation_Result.RESULT_FORBIDDEN,
                ),
            )

            self.assertEqual(license_components[22].component_name_version, "email-validator:2.1.1")
            self.assertEqual(
                license_components[22].license_expression,
                "GPL-3.0-or-later WITH Bison-exception-2.2",
            )
            self.assertEqual(
                license_components[22].evaluation_result,
                License_Policy_Evaluation_Result.RESULT_UNKNOWN,
            )
            self.assertEqual(
                license_components[22].numerical_evaluation_result,
                License_Policy_Evaluation_Result.NUMERICAL_RESULTS.get(
                    License_Policy_Evaluation_Result.RESULT_UNKNOWN,
                ),
            )

        # --- Fourth import with ignoring the PiPy packages ---

        license_policy = License_Policy.objects.get(name="Standard")
        license_policy.ignore_component_types = "npm, pypi"
        license_policy.save()

        file_upload_parameters = FileUploadParameters(
            product=product,
            branch=branch,
            file=File(
                open(
                    "unittests/import_observations/parsers/cyclone_dx/files/changed/licenses_1.json",
                    "r",
                )
            ),
            service=service,
            docker_image_name_tag=docker_image_name_tag,
            endpoint_url=endpoint_url,
            kubernetes_cluster=kubernetes_cluster,
            suppress_licenses=suppress_licenses,
        )

        (
            new_observations,
            updated_observations,
            resolved_observations,
            new_license_objects,
            updated_license_objects,
            deleted_license_objects,
        ) = file_upload_observations(file_upload_parameters)

        settings = Settings.load()
        if settings.feature_license_management and not suppress_licenses:
            self.assertEqual(new_observations, 0)
            self.assertEqual(updated_observations, 0)
            self.assertEqual(resolved_observations, 0)
            self.assertEqual(new_license_objects, 0)
            self.assertEqual(updated_license_objects, 67)
            self.assertEqual(deleted_license_objects, 0)

            license_components = License_Component.objects.filter(product=1).order_by("id")
            self.assertEqual(len(license_components), 67)

            self.assertEqual(
                license_components[64].component_name_version,
                "argon2-cffi-bindings:21.2.1",
            )
            self.assertEqual(license_components[64].license, License.objects.get(spdx_id="MIT"))
            self.assertEqual(license_components[64].non_spdx_license, "")
            self.assertEqual(
                license_components[64].evaluation_result,
                License_Policy_Evaluation_Result.RESULT_IGNORED,
            )
            self.assertEqual(
                license_components[64].numerical_evaluation_result,
                License_Policy_Evaluation_Result.NUMERICAL_RESULTS.get(
                    License_Policy_Evaluation_Result.RESULT_IGNORED,
                ),
            )

            self.assertEqual(license_components[2].component_name_version, "asgiref:3.8.1")
            self.assertEqual(license_components[2].license, None)
            self.assertEqual(license_components[2].non_spdx_license, "0BSD, BSD-3-Clause")
            self.assertEqual(
                license_components[2].evaluation_result,
                License_Policy_Evaluation_Result.RESULT_IGNORED,
            )
            self.assertEqual(
                license_components[2].numerical_evaluation_result,
                License_Policy_Evaluation_Result.NUMERICAL_RESULTS.get(
                    License_Policy_Evaluation_Result.RESULT_IGNORED,
                ),
            )
        else:
            self.assertEqual(new_observations, 0)
            self.assertEqual(updated_observations, 0)
            self.assertEqual(resolved_observations, 0)
            self.assertEqual(new_license_objects, 0)
            self.assertEqual(updated_license_objects, 0)
            self.assertEqual(deleted_license_objects, 0)

            license_components = License_Component.objects.filter(product=1)
            self.assertEqual(len(license_components), 0)


class RequestMock:
    def __init__(self, user):
        self.user = user
