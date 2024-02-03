from unittest.mock import call, patch

from django.core.files.base import File
from django.core.management import call_command

from application.access_control.models import User
from application.core.models import (
    Branch,
    Evidence,
    Observation,
    Observation_Log,
    Parser,
    Product,
    Reference,
)
from application.core.types import Severity, Status
from application.import_observations.apps import _register_parser
from application.import_observations.models import Vulnerability_Check
from application.import_observations.services.import_observations import (
    FileUploadParameters,
    file_upload_observations,
)
from application.rules.models import Rule
from unittests.base_test_case import BaseTestCase


class TestImportObservations(BaseTestCase):
    def setUp(self):
        Observation.objects.all().delete()
        Observation_Log.objects.all().delete()
        Rule.objects.all().delete()
        Vulnerability_Check.objects.all().delete()
        call_command("loaddata", "unittests/fixtures/import_observations_fixtures.json")
        _register_parser("sarif")
        super().setUp()

    @patch("application.commons.services.global_request.get_current_request")
    @patch(
        "application.import_observations.services.import_observations.check_security_gate"
    )
    @patch(
        "application.import_observations.services.import_observations.set_repository_default_branch"
    )
    @patch(
        "application.import_observations.services.import_observations.push_observations_to_issue_tracker"
    )
    @patch(
        "application.import_observations.services.import_observations.epss_apply_observation"
    )
    @patch(
        "application.import_observations.services.import_observations.find_potential_duplicates"
    )
    def test_file_upload_observations_with_branch(
        self,
        mock_find_potential_duplicates,
        mock_epss_apply_observation,
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
        )

        product = Product.objects.get(id=1)
        mock_check_security_gate.assert_has_calls([call(product), call(product)])
        mock_set_repository_default_branch.assert_has_calls(
            [call(product), call(product)]
        )
        self.assertEqual(mock_push_observations_to_issue_tracker.call_count, 2)
        self.assertEqual(mock_epss_apply_observation.call_count, 4)
        self.assertEqual(mock_find_potential_duplicates.call_count, 2)

    @patch("application.commons.services.global_request.get_current_request")
    @patch(
        "application.import_observations.services.import_observations.check_security_gate"
    )
    @patch(
        "application.import_observations.services.import_observations.set_repository_default_branch"
    )
    @patch(
        "application.import_observations.services.import_observations.push_observations_to_issue_tracker"
    )
    @patch(
        "application.import_observations.services.import_observations.epss_apply_observation"
    )
    @patch(
        "application.import_observations.services.import_observations.find_potential_duplicates"
    )
    def test_file_upload_observations_without_branch(
        self,
        mock_find_potential_duplicates,
        mock_epss_apply_observation,
        mock_push_observations_to_issue_tracker,
        mock_set_repository_default_branch,
        mock_check_security_gate,
        mock_get_current_request,
    ):
        mock_get_current_request.return_value = RequestMock(User.objects.get(id=1))
        self._file_upload_observations(None, None, None, None)

        product = Product.objects.get(id=1)
        mock_check_security_gate.assert_has_calls([call(product), call(product)])
        mock_set_repository_default_branch.assert_has_calls(
            [call(product), call(product)]
        )
        self.assertEqual(mock_push_observations_to_issue_tracker.call_count, 2)
        self.assertEqual(mock_epss_apply_observation.call_count, 4)
        self.assertEqual(mock_find_potential_duplicates.call_count, 2)

    def _file_upload_observations(
        self, branch, service, docker_image_name_tag, endpoint_url
    ):
        # --- First import ---

        file_upload_parameters = FileUploadParameters(
            product=Product.objects.get(id=1),
            branch=branch,
            parser=Parser.objects.get(id=1),
            file=File(open("unittests/fixtures/data_1/bandit.sarif", "r")),
            service=service,
            docker_image_name_tag=docker_image_name_tag,
            endpoint_url=endpoint_url,
        )

        new, updated, resolved = file_upload_observations(file_upload_parameters)

        self.assertEqual(new, 2)
        self.assertEqual(updated, 0)
        self.assertEqual(resolved, 0)

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
            self.assertEqual(
                observations[0].origin_docker_image_name_tag, docker_image_name_tag
            )
        else:
            self.assertEqual(observations[0].origin_docker_image_name_tag, "")
        if endpoint_url:
            self.assertEqual(observations[0].origin_endpoint_url, endpoint_url)
        else:
            self.assertEqual(observations[0].origin_endpoint_url, "")

        self.assertEqual(observations[0].current_status, Status.STATUS_OPEN)
        self.assertEqual(observations[1].current_status, Status.STATUS_OPEN)
        self.assertEqual(observations[2].current_status, Status.STATUS_NOT_AFFECTED)

        observation_logs = Observation_Log.objects.filter(
            observation__product=1
        ).order_by("id")
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

        references = Reference.objects.filter(observation__product=product).order_by(
            "id"
        )
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
            parser=Parser.objects.get(id=1),
            file=File(open("unittests/fixtures/data_2/bandit.sarif", "r")),
            service=service,
            docker_image_name_tag=docker_image_name_tag,
            endpoint_url=endpoint_url,
        )

        new, updated, resolved = file_upload_observations(file_upload_parameters)

        self.assertEqual(new, 0)
        self.assertEqual(updated, 1)
        self.assertEqual(resolved, 1)

        observations = Observation.objects.filter(product=1).order_by("id")
        self.assertEqual(len(observations), 3)

        self.assertEqual(observations[0].current_status, Status.STATUS_RESOLVED)
        self.assertEqual(observations[1].current_status, Status.STATUS_OPEN)
        self.assertEqual(observations[2].current_status, Status.STATUS_RESOLVED)

        observation_logs = Observation_Log.objects.filter(
            observation__product=1
        ).order_by("id")
        self.assertEqual(len(observation_logs), 7)

        self.assertEqual(observation_logs[4].observation, observations[1])
        self.assertEqual(observation_logs[4].severity, Severity.SEVERITY_HIGH)
        self.assertEqual(observation_logs[4].status, "")
        self.assertEqual(observation_logs[4].comment, "Updated by parser")

        self.assertEqual(observation_logs[5].observation, observations[0])
        self.assertEqual(observation_logs[5].severity, "")
        self.assertEqual(observation_logs[5].status, Status.STATUS_RESOLVED)
        self.assertEqual(
            observation_logs[5].comment, "Observation not found in latest scan"
        )

        self.assertEqual(observation_logs[6].observation, observations[2])
        self.assertEqual(observation_logs[6].severity, "")
        self.assertEqual(observation_logs[6].status, Status.STATUS_RESOLVED)
        self.assertEqual(
            observation_logs[6].comment, "Observation not found in latest scan"
        )

        references = Reference.objects.filter(observation__product=product).order_by(
            "id"
        )
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


class RequestMock:
    def __init__(self, user):
        self.user = user
