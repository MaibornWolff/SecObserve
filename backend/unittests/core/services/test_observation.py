from copy import deepcopy

from application.core.models import Observation
from application.core.services.observation import (
    _get_string_to_hash,
    get_current_severity,
    get_current_status,
    get_identity_hash,
    normalize_observation_fields,
)
from application.core.types import Severity, Status
from unittests.base_test_case import BaseTestCase


class TestObservation(BaseTestCase):
    def setUp(self) -> None:
        self.addTypeEqualityFunc(Observation, _observation_equal)
        return super().setUp()

    # --- identity hash ---

    def test_get_identity_hash(self):
        observation = Observation(title="observation")
        self.assertEqual(
            "772c6953848bf5b19aedf9a34ccb066f31eacca29bdbfcb1b9821765f1060149",
            get_identity_hash(observation),
        )

    def test_get_string_to_hash_empty(self):
        observation = Observation(title="empty")
        self.assertEqual("empty", _get_string_to_hash(observation))

    def test_get_string_to_hash_full(self):
        observation = Observation(
            title="full",
            origin_component_name_version="component_name:version",
            origin_docker_image_name="docker_image_name",
            origin_docker_image_name_tag="docker_image_name:tag",
            origin_endpoint_url="endpoint_url",
            origin_service_name="service_name",
            origin_source_file="source_file",
            origin_source_line_start=1,
            origin_source_line_end=999,
        )
        self.assertEqual(
            "fullcomponent_name:versiondocker_image_nameendpoint_urlservice_namesource_file1999",
            _get_string_to_hash(observation),
        )

    def test_get_string_to_hash_intermediate(self):
        observation = Observation(
            title="intermediate",
            origin_component_name="component_name",
            origin_component_version="component_version",
            origin_docker_image_name_tag="docker_image_name:tag",
        )
        self.assertEqual(
            "intermediatecomponent_namecomponent_versiondocker_image_name:tag",
            _get_string_to_hash(observation),
        )

    # --- get_current_severity ---

    def test_get_current_severity_unkown(self):
        observation = Observation(
            title="unkown",
            current_severity=Severity.SEVERITY_NONE,
        )
        self.assertEqual(Severity.SEVERITY_UNKOWN, get_current_severity(observation))

    def test_get_current_severity_assessment(self):
        observation = Observation(
            title="assessment_severity",
            current_severity=Severity.SEVERITY_NONE,
            parser_severity=Severity.SEVERITY_LOW,
            rule_severity=Severity.SEVERITY_LOW,
            assessment_severity=Severity.SEVERITY_MEDIUM,
            cvss3_score=9.5,
        )
        self.assertEqual(Severity.SEVERITY_MEDIUM, get_current_severity(observation))

    def test_get_current_severity_rule(self):
        observation = Observation(
            title="rule_severity",
            current_severity=Severity.SEVERITY_NONE,
            parser_severity=Severity.SEVERITY_LOW,
            rule_severity=Severity.SEVERITY_MEDIUM,
            cvss3_score=9.5,
        )
        self.assertEqual(Severity.SEVERITY_MEDIUM, get_current_severity(observation))

    def test_get_current_severity_parser(self):
        observation = Observation(
            title="parser_severity",
            current_severity=Severity.SEVERITY_NONE,
            parser_severity=Severity.SEVERITY_LOW,
            cvss3_score=9.5,
        )
        self.assertEqual(Severity.SEVERITY_LOW, get_current_severity(observation))

    def test_get_current_severity_cvss_critical(self):
        observation = Observation(
            title="parser_severity",
            current_severity=Severity.SEVERITY_NONE,
            cvss3_score=9,
        )
        self.assertEqual(Severity.SEVERITY_CRITICAL, get_current_severity(observation))

    def test_get_current_severity_cvss_high(self):
        observation = Observation(
            title="parser_severity",
            current_severity=Severity.SEVERITY_NONE,
            cvss3_score=7,
        )
        self.assertEqual(Severity.SEVERITY_HIGH, get_current_severity(observation))

    def test_get_current_severity_cvss_medium(self):
        observation = Observation(
            title="parser_severity",
            current_severity=Severity.SEVERITY_NONE,
            cvss3_score=4,
        )
        self.assertEqual(Severity.SEVERITY_MEDIUM, get_current_severity(observation))

    def test_get_current_severity_cvss_low(self):
        observation = Observation(
            title="parser_severity",
            current_severity=Severity.SEVERITY_NONE,
            cvss3_score=0.1,
        )
        self.assertEqual(Severity.SEVERITY_LOW, get_current_severity(observation))

    def test_get_current_severity_cvss_none(self):
        observation = Observation(
            title="parser_severity",
            current_severity=Severity.SEVERITY_MEDIUM,
            cvss3_score=0,
        )
        self.assertEqual(Severity.SEVERITY_NONE, get_current_severity(observation))

    # --- get_current_status ---

    def test_get_current_status_open(self):
        observation = Observation(
            title="open",
            current_status=Status.STATUS_RESOLVED,
        )
        self.assertEqual(Status.STATUS_OPEN, get_current_status(observation))

    def test_get_current_status_assessment(self):
        observation = Observation(
            title="assessment_status",
            current_status=Status.STATUS_RESOLVED,
            parser_status=Status.STATUS_NOT_AFFECTED,
            rule_status=Status.STATUS_DUPLICATE,
            assessment_status=Status.STATUS_FALSE_POSITIVE,
            cvss3_score=9.5,
        )
        self.assertEqual(Status.STATUS_FALSE_POSITIVE, get_current_status(observation))

    def test_get_current_status_rule(self):
        observation = Observation(
            title="assessment_status",
            current_status=Status.STATUS_RESOLVED,
            parser_status=Status.STATUS_NOT_AFFECTED,
            rule_status=Status.STATUS_DUPLICATE,
            cvss3_score=9.5,
        )
        self.assertEqual(Status.STATUS_DUPLICATE, get_current_status(observation))

    def test_get_current_status_parser(self):
        observation = Observation(
            title="parser_status",
            current_status=Status.STATUS_RESOLVED,
            parser_status=Status.STATUS_NOT_AFFECTED,
        )
        self.assertEqual(Status.STATUS_NOT_AFFECTED, get_current_status(observation))

    # --- normalize_observation_fields ---

    def test_normalize_observation_fields_empty(self):
        before_observation = Observation(title="empty")
        after_observation = deepcopy(before_observation)

        before_observation.current_severity = Severity.SEVERITY_UNKOWN
        before_observation.numerical_severity = 6
        before_observation.current_status = Status.STATUS_OPEN

        normalize_observation_fields(after_observation)
        self.assertEqual(before_observation, after_observation)

    def test_normalize_observation_fields_none(self):
        before_observation = Observation(title="empty")
        after_observation = deepcopy(before_observation)
        for key in dir(after_observation):
            if (
                key not in _get_excludes()
                and not callable(getattr(after_observation, key))
                and not key.startswith("_")
            ):
                value = after_observation.__dict__.get(key)
                if value == "":
                    after_observation.__dict__[key] = None
                    value = None

        before_observation.current_severity = Severity.SEVERITY_UNKOWN
        before_observation.numerical_severity = 6
        before_observation.current_status = Status.STATUS_OPEN

        normalize_observation_fields(after_observation)
        self.assertEqual(before_observation, after_observation)

    def test_normalize_observation_fields_selected_fields(self):
        before_observation = Observation(
            title="empty",
            description="desc\n\n",
            origin_endpoint_url="https://www.example.com/subpath?var=1",
        )
        after_observation = deepcopy(before_observation)

        before_observation.current_severity = Severity.SEVERITY_UNKOWN
        before_observation.numerical_severity = 6
        before_observation.current_status = Status.STATUS_OPEN
        before_observation.description = "desc"
        before_observation.origin_endpoint_scheme = "https"
        before_observation.origin_endpoint_hostname = "www.example.com"
        before_observation.origin_endpoint_path = "/subpath"
        before_observation.origin_endpoint_query = "var=1"

        normalize_observation_fields(after_observation)
        self.assertEqual(before_observation, after_observation)

    def test_normalize_observation_fields_origin_component_name_version_1(self):
        before_observation = Observation(
            title="empty", origin_component_name_version="component_name"
        )
        after_observation = deepcopy(before_observation)

        before_observation.current_severity = Severity.SEVERITY_UNKOWN
        before_observation.numerical_severity = 6
        before_observation.current_status = Status.STATUS_OPEN
        before_observation.origin_component_name = "component_name"
        before_observation.origin_component_version = ""

        normalize_observation_fields(after_observation)
        self.assertEqual(before_observation, after_observation)

    def test_normalize_observation_fields_origin_component_name_version_2(self):
        before_observation = Observation(
            title="empty",
            origin_component_name_version="component_name:component_version",
        )
        after_observation = deepcopy(before_observation)

        before_observation.current_severity = Severity.SEVERITY_UNKOWN
        before_observation.numerical_severity = 6
        before_observation.current_status = Status.STATUS_OPEN
        before_observation.origin_component_name = "component_name"
        before_observation.origin_component_version = "component_version"

        normalize_observation_fields(after_observation)
        self.assertEqual(before_observation, after_observation)

    def test_normalize_observation_fields_origin_component_name_component_version(self):
        before_observation = Observation(
            title="empty",
            origin_component_name="component_name",
            origin_component_version="component_version",
        )
        after_observation = deepcopy(before_observation)

        before_observation.current_severity = Severity.SEVERITY_UNKOWN
        before_observation.numerical_severity = 6
        before_observation.current_status = Status.STATUS_OPEN
        before_observation.origin_component_name_version = (
            "component_name:component_version"
        )

        normalize_observation_fields(after_observation)
        self.assertEqual(before_observation, after_observation)

    def test_normalize_observation_fields_origin_component_name(self):
        before_observation = Observation(
            title="empty", origin_component_name="component_name"
        )
        after_observation = deepcopy(before_observation)

        before_observation.current_severity = Severity.SEVERITY_UNKOWN
        before_observation.numerical_severity = 6
        before_observation.current_status = Status.STATUS_OPEN
        before_observation.origin_component_name_version = "component_name"

        normalize_observation_fields(after_observation)
        self.assertEqual(before_observation, after_observation)

    def test_normalize_observation_fields_origin_docker_image_name_tag_1(self):
        before_observation = Observation(
            title="empty", origin_docker_image_name_tag="docker_image_name"
        )
        after_observation = deepcopy(before_observation)

        before_observation.current_severity = Severity.SEVERITY_UNKOWN
        before_observation.numerical_severity = 6
        before_observation.current_status = Status.STATUS_OPEN
        before_observation.origin_docker_image_name = "docker_image_name"
        before_observation.origin_docker_image_tag = ""
        before_observation.origin_docker_image_name_tag_short = "docker_image_name"
        normalize_observation_fields(after_observation)
        self.assertEqual(before_observation, after_observation)

    def test_normalize_observation_fields_origin_docker_image_name_tag_2(self):
        before_observation = Observation(
            title="empty",
            origin_docker_image_name_tag="docker_image_name:docker_image_tag",
        )
        after_observation = deepcopy(before_observation)

        before_observation.current_severity = Severity.SEVERITY_UNKOWN
        before_observation.numerical_severity = 6
        before_observation.current_status = Status.STATUS_OPEN
        before_observation.origin_docker_image_name = "docker_image_name"
        before_observation.origin_docker_image_tag = "docker_image_tag"
        before_observation.origin_docker_image_name_tag_short = (
            "docker_image_name:docker_image_tag"
        )

        normalize_observation_fields(after_observation)
        self.assertEqual(before_observation, after_observation)

    def test_normalize_observation_fields_origin_docker_image_name_docker_image_tag(
        self,
    ):
        before_observation = Observation(
            title="empty",
            origin_docker_image_name="docker_image_name",
            origin_docker_image_tag="docker_image_tag",
        )
        after_observation = deepcopy(before_observation)

        before_observation.current_severity = Severity.SEVERITY_UNKOWN
        before_observation.numerical_severity = 6
        before_observation.current_status = Status.STATUS_OPEN
        before_observation.origin_docker_image_name_tag = (
            "docker_image_name:docker_image_tag"
        )
        before_observation.origin_docker_image_name_tag_short = (
            "docker_image_name:docker_image_tag"
        )

        normalize_observation_fields(after_observation)
        self.assertEqual(before_observation, after_observation)

    def test_normalize_observation_fields_origin_docker_image_name(self):
        before_observation = Observation(
            title="empty", origin_docker_image_name="docker_image_name"
        )
        after_observation = deepcopy(before_observation)

        before_observation.current_severity = Severity.SEVERITY_UNKOWN
        before_observation.numerical_severity = 6
        before_observation.current_status = Status.STATUS_OPEN
        before_observation.origin_docker_image_name_tag = "docker_image_name"
        before_observation.origin_docker_image_name_tag_short = "docker_image_name"

        normalize_observation_fields(after_observation)
        self.assertEqual(before_observation, after_observation)


def _observation_equal(expected_observation, actual_observation, msg=None):
    for key in dir(expected_observation):
        if (
            key not in _get_excludes()
            and not callable(getattr(expected_observation, key))
            and not key.startswith("_")
        ):
            expected_value = expected_observation.__dict__.get(key)
            actual_value = actual_observation.__dict__.get(key)
            if expected_value != actual_value:
                raise AssertionError(
                    f"Key {key}: expected: {expected_value}, actual: {actual_value}"
                )


def _get_excludes():
    return [
        "pk",
        "objects",
        "unsaved_references",
        "unsaved_evidences",
        "NUMERICAL_SEVERITIES",
        "SEVERITY_CHOICES",
        "SEVERITY_CRITICAL",
        "SEVERITY_HIGH",
        "SEVERITY_LOW",
        "SEVERITY_MEDIUM",
        "SEVERITY_NONE",
        "SEVERITY_UNKOWN",
        "STATUS_CHOICES",
        "STATUS_DUPLICATE",
        "STATUS_FALSE_POSITIVE",
        "STATUS_IN_REVIEW",
        "STATUS_NOT_AFFECTED",
        "STATUS_OPEN",
        "STATUS_RESOLVED",
        "STATUS_RISK_ACCEPTED",
        "parser",
        "product",
        "identity_hash",
    ]
