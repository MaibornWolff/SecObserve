import hashlib
from urllib.parse import urlparse

from django.apps import apps
from django.db.models.fields import CharField, TextField

from application.core.types import Severity, Status

# Parameter observation cannot be typed, because some methods are used in the model class


def get_identity_hash(observation) -> str:
    hash_string = _get_string_to_hash(observation)

    return hashlib.sha256(hash_string.casefold().encode("utf-8").strip()).hexdigest()


def _get_string_to_hash(observation):  # pylint: disable=too-many-branches
    hash_string = observation.title

    if observation.origin_component_name_version:
        hash_string += observation.origin_component_name_version
    else:
        if observation.origin_component_name:
            hash_string += observation.origin_component_name
        if observation.origin_component_version:
            hash_string += observation.origin_component_version

    if observation.origin_docker_image_name:
        hash_string += observation.origin_docker_image_name
    elif observation.origin_docker_image_name_tag:
        hash_string += observation.origin_docker_image_name_tag

    if observation.origin_endpoint_url:
        hash_string += observation.origin_endpoint_url

    if observation.origin_service_name:
        hash_string += observation.origin_service_name

    if observation.origin_source_file:
        hash_string += observation.origin_source_file
    if observation.origin_source_line_start:
        hash_string += str(observation.origin_source_line_start)
    if observation.origin_source_line_end:
        hash_string += str(observation.origin_source_line_end)

    if observation.origin_cloud_provider:
        hash_string += observation.origin_cloud_provider
    if observation.origin_cloud_account_subscription_project:
        hash_string += observation.origin_cloud_account_subscription_project
    if observation.origin_cloud_resource:
        hash_string += observation.origin_cloud_resource

    return hash_string


def get_current_severity(observation) -> str:
    if observation.assessment_severity:
        return observation.assessment_severity

    if observation.rule_severity:
        return observation.rule_severity

    if observation.parser_severity:
        return observation.parser_severity

    return _get_cvss3_severity(observation.cvss3_score)


def _get_cvss3_severity(cvss3_score: int):
    if cvss3_score is None:
        return Severity.SEVERITY_UNKOWN

    if cvss3_score >= 9:
        return Severity.SEVERITY_CRITICAL

    if cvss3_score >= 7:
        return Severity.SEVERITY_HIGH

    if cvss3_score >= 4:
        return Severity.SEVERITY_MEDIUM

    if cvss3_score >= 0.1:
        return Severity.SEVERITY_LOW

    return Severity.SEVERITY_NONE


def get_current_status(observation) -> str:
    if observation.parser_status == Status.STATUS_RESOLVED:
        return observation.parser_status

    if observation.assessment_status:
        return observation.assessment_status

    if observation.rule_status:
        return observation.rule_status

    if observation.parser_status:
        return observation.parser_status

    return Status.STATUS_OPEN


def normalize_observation_fields(observation) -> None:
    normalize_origin_component(observation)
    normalize_origin_docker(observation)
    normalize_origin_endpoint(observation)
    normalize_origin_cloud(observation)

    normalize_severity(observation)
    normalize_status(observation)

    normalize_description(observation)

    if observation.recommendation is None:
        observation.recommendation = ""
    if observation.scanner_observation_id is None:
        observation.scanner_observation_id = ""
    if observation.origin_service_name is None:
        observation.origin_service_name = ""
    if observation.origin_source_file is None:
        observation.origin_source_file = ""
    if observation.cvss3_vector is None:
        observation.cvss3_vector = ""
    if observation.scanner is None:
        observation.scanner = ""
    if observation.api_configuration_name is None:
        observation.api_configuration_name = ""
    if observation.upload_filename is None:
        observation.upload_filename = ""
    if observation.vulnerability_id is None:
        observation.vulnerability_id = ""
    if observation.issue_tracker_issue_id is None:
        observation.issue_tracker_issue_id = ""
    if observation.issue_tracker_jira_initial_status is None:
        observation.issue_tracker_jira_initial_status = ""


def normalize_description(observation):
    if observation.description is None:
        observation.description = ""
    else:
        # Newlines at the end of the description are removed
        while observation.description.endswith("\n"):
            observation.description = observation.description[:-1]


def normalize_origin_component(observation):  # pylint: disable=too-many-branches
    if not observation.origin_component_name_version:
        if observation.origin_component_name and observation.origin_component_version:
            observation.origin_component_name_version = (
                observation.origin_component_name
                + ":"
                + observation.origin_component_version
            )
        elif observation.origin_component_name:
            observation.origin_component_name_version = (
                observation.origin_component_name
            )
    else:
        component_parts = observation.origin_component_name_version.split(":")
        if len(component_parts) == 3:
            observation.origin_component_name = (
                f"{component_parts[0]}:{component_parts[1]}"
            )
            observation.origin_component_version = component_parts[2]
        elif len(component_parts) == 2:
            observation.origin_component_name = component_parts[0]
            observation.origin_component_version = component_parts[1]
        elif len(component_parts) == 1:
            observation.origin_component_name = (
                observation.origin_component_name_version
            )
            observation.origin_component_version = None

    if observation.origin_component_name_version is None:
        observation.origin_component_name_version = ""
    if observation.origin_component_name is None:
        observation.origin_component_name = ""
    if observation.origin_component_version is None:
        observation.origin_component_version = ""
    if observation.origin_component_purl is None:
        observation.origin_component_purl = ""
    if observation.origin_component_cpe is None:
        observation.origin_component_cpe = ""
    if observation.origin_component_dependencies is None:
        observation.origin_component_dependencies = ""


def normalize_origin_docker(observation):
    if not observation.origin_docker_image_name_tag:
        _normalize_origin_docker_image_name(observation)
    else:
        _normalize_origin_docker_image_name_tag(observation)

    if observation.origin_docker_image_name_tag:
        origin_docker_image_name_tag_parts = (
            observation.origin_docker_image_name_tag.split("/")
        )
        observation.origin_docker_image_name_tag_short = (
            origin_docker_image_name_tag_parts[
                len(origin_docker_image_name_tag_parts) - 1
            ].strip()
        )
    else:
        observation.origin_docker_image_name_tag_short = ""

    if observation.origin_docker_image_name_tag is None:
        observation.origin_docker_image_name_tag = ""
    if observation.origin_docker_image_name is None:
        observation.origin_docker_image_name = ""
    if observation.origin_docker_image_tag is None:
        observation.origin_docker_image_tag = ""
    if observation.origin_docker_image_digest is None:
        observation.origin_docker_image_digest = ""


def _normalize_origin_docker_image_name(observation):
    if observation.origin_docker_image_name and not observation.origin_docker_image_tag:
        docker_image_parts = observation.origin_docker_image_name.split(":")
        if len(docker_image_parts) == 2:
            observation.origin_docker_image_name = docker_image_parts[0]
            observation.origin_docker_image_tag = docker_image_parts[1]

    if observation.origin_docker_image_name and observation.origin_docker_image_tag:
        observation.origin_docker_image_name_tag = (
            observation.origin_docker_image_name
            + ":"
            + observation.origin_docker_image_tag
        )
    else:
        observation.origin_docker_image_name_tag = observation.origin_docker_image_name


def _normalize_origin_docker_image_name_tag(observation):
    docker_image_parts = observation.origin_docker_image_name_tag.split(":")
    if len(docker_image_parts) == 2:
        observation.origin_docker_image_name = docker_image_parts[0]
        observation.origin_docker_image_tag = docker_image_parts[1]
    else:
        observation.origin_docker_image_name = observation.origin_docker_image_name_tag


def normalize_origin_endpoint(observation):
    if observation.origin_endpoint_url:
        parse_result = urlparse(observation.origin_endpoint_url)
        observation.origin_endpoint_scheme = parse_result.scheme
        observation.origin_endpoint_hostname = parse_result.hostname
        observation.origin_endpoint_port = parse_result.port
        observation.origin_endpoint_path = parse_result.path
        observation.origin_endpoint_params = parse_result.params
        observation.origin_endpoint_query = parse_result.query
        observation.origin_endpoint_fragment = parse_result.fragment
    else:
        observation.origin_endpoint_scheme = ""
        observation.origin_endpoint_hostname = ""
        observation.origin_endpoint_port = None
        observation.origin_endpoint_path = ""
        observation.origin_endpoint_params = ""
        observation.origin_endpoint_query = ""
        observation.origin_endpoint_fragment = ""

    if observation.origin_endpoint_url is None:
        observation.origin_endpoint_url = ""
    if observation.origin_endpoint_scheme is None:
        observation.origin_endpoint_scheme = ""
    if observation.origin_endpoint_hostname is None:
        observation.origin_endpoint_hostname = ""
    if observation.origin_endpoint_path is None:
        observation.origin_endpoint_path = ""
    if observation.origin_endpoint_params is None:
        observation.origin_endpoint_params = ""
    if observation.origin_endpoint_query is None:
        observation.origin_endpoint_query = ""
    if observation.origin_endpoint_fragment is None:
        observation.origin_endpoint_fragment = ""


def normalize_origin_cloud(observation):
    if observation.origin_cloud_provider is None:
        observation.origin_cloud_provider = ""
    if observation.origin_cloud_account_subscription_project is None:
        observation.origin_cloud_account_subscription_project = ""
    if observation.origin_cloud_resource is None:
        observation.origin_cloud_resource = ""
    if observation.origin_cloud_resource_type is None:
        observation.origin_cloud_resource_type = ""

    observation.origin_cloud_qualified_resource = ""
    if observation.origin_cloud_account_subscription_project:
        observation.origin_cloud_qualified_resource = (
            (observation.origin_cloud_account_subscription_project[:119] + "...")
            if len(observation.origin_cloud_account_subscription_project) > 122
            else observation.origin_cloud_account_subscription_project
        )
    if (
        observation.origin_cloud_account_subscription_project
        and observation.origin_cloud_resource
    ):
        observation.origin_cloud_qualified_resource += " / "
    if observation.origin_cloud_resource:
        observation.origin_cloud_qualified_resource += (
            (observation.origin_cloud_resource[:119] + "...")
            if len(observation.origin_cloud_resource) > 122
            else observation.origin_cloud_resource
        )


def normalize_severity(observation):
    if observation.current_severity is None:
        observation.current_severity = ""
    if observation.assessment_severity is None:
        observation.assessment_severity = ""
    if observation.rule_severity is None:
        observation.rule_severity = ""
    if observation.parser_severity is None:
        observation.parser_severity = ""
    if observation.parser_severity:
        if (
            observation.parser_severity,
            observation.parser_severity,
        ) not in Severity.SEVERITY_CHOICES:
            observation.parser_severity = Severity.SEVERITY_UNKOWN

    observation.current_severity = get_current_severity(observation)

    observation.numerical_severity = Severity.NUMERICAL_SEVERITIES.get(
        observation.current_severity
    )


def normalize_status(observation):
    if observation.current_status is None:
        observation.current_status = ""
    if observation.assessment_status is None:
        observation.assessment_status = ""
    if observation.rule_status is None:
        observation.rule_status = ""
    if observation.parser_status is None:
        observation.parser_status = ""

    observation.current_status = get_current_status(observation)


def clip_fields(model: str, my_object) -> None:
    Model = apps.get_model("core", model)
    for field in Model._meta.get_fields():
        if isinstance(field, (CharField, TextField)):
            _, _, _, key_args = field.deconstruct()
            max_length = key_args.get("max_length")
            if max_length:
                value = getattr(my_object, field.name)
                if value and len(value) > max_length:
                    setattr(my_object, field.name, value[: max_length - 4] + " ...")
                    value = getattr(my_object, field.name)
                    if value.count("```") == 1:
                        # There is an open code block, that we have to close
                        setattr(
                            my_object,
                            field.name,
                            value[: max_length - 9] + "\n```\n\n...",
                        )
