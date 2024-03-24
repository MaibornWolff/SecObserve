import re
from decimal import Decimal

import validators
from cvss import CVSS3, CVSSError
from packageurl import PackageURL
from rest_framework.serializers import ValidationError

from application.core.models import Observation
from application.core.services.observation import get_cvss3_severity


def get_branch_name(observation: Observation) -> str:
    if not observation.branch:
        return ""

    return observation.branch.name


def get_scanner_name(observation: Observation) -> str:
    if not observation.scanner:
        return ""

    scanner_parts = observation.scanner.split("/")
    return scanner_parts[0].strip()


def get_origin_component_name_version(observation: Observation) -> str:
    if not observation.origin_component_name:
        return ""

    origin_component_name_version_with_type = observation.origin_component_name_version
    if observation.origin_component_purl:
        purl = PackageURL.from_string(observation.origin_component_purl)
        if purl.type:
            origin_component_name_version_with_type += f" ({purl.type})"

    return origin_component_name_version_with_type


def validate_url(url: str) -> str:
    if url and not validators.url(url):
        raise ValidationError("Not a valid URL")

    return url


def validate_cvss3_vector(cvss3_vector):
    if cvss3_vector:
        try:
            cvss3 = CVSS3(cvss3_vector)
            cvss3_vector = cvss3.clean_vector()
        except CVSSError as e:
            raise ValidationError(str(e))  # pylint: disable=raise-missing-from
        # The CVSSError itself is not relevant and must not be re-raised

    return cvss3_vector


def validate_cvss_and_severity(attrs):
    base_score = None
    if attrs.get("cvss3_vector"):
        cvss3 = CVSS3(attrs.get("cvss3_vector"))
        base_score = Decimal(cvss3.scores()[0]).quantize(Decimal(".0"))

    cvss3_score = attrs.get("cvss3_score")
    if cvss3_score is not None:
        if base_score is not None and base_score != cvss3_score:
            raise ValidationError(
                f"Score from CVSS3 vector ({base_score}) is different than CVSS3 score ({cvss3_score})"
            )
    else:
        attrs["cvss3_score"] = base_score

    cvss3_score = attrs.get("cvss3_score")
    cvss3_severity = (
        get_cvss3_severity(cvss3_score) if cvss3_score is not None else None
    )
    parser_severity = attrs.get("parser_severity")

    if parser_severity:
        if cvss3_severity and parser_severity != cvss3_severity:
            raise ValidationError(
                f"Severity ({parser_severity}) is different than severity from CVSS3 score ({cvss3_severity})"
            )
    else:
        if not cvss3_severity:
            raise ValidationError(
                "Either Severity, CVSS3 score or CVSS3 vector has to be set"
            )


def validate_purl(purl: str) -> str:
    if purl:
        try:
            PackageURL.from_string(purl)
        except ValueError as e:
            raise ValidationError(str(e))  # pylint: disable=raise-missing-from
            # The initial exception is not really relevant, we only need its message

    return purl


def validate_cpe23(cpe23: str) -> str:
    if cpe23:
        # Regex taken from https://csrc.nist.gov/schema/cpe/2.3/cpe-naming_2.3.xsd
        if not re.match(
            r"""cpe:2\.3:[aho\*\-](:(((\?*|\*?)([a-zA-Z0-9\-\._]|(\\[\\\*\?!"#$$%&'\(\)\+,/:;<=>@\[\]\^`\{\|}~]))+(\?*|\*?))|[\*\-])){5}(:(([a-zA-Z]{2,3}(-([a-zA-Z]{2}|[0-9]{3}))?)|[\*\-]))(:(((\?*|\*?)([a-zA-Z0-9\-\._]|(\\[\\\*\?!"#$$%&'\(\)\+,/:;<=>@\[\]\^`\{\|}~]))+(\?*|\*?))|[\*\-])){4}""",  # noqa: E501 pylint: disable=line-too-long
            cpe23,
        ):
            raise ValidationError("Not a valid CPE 2.3")
    return cpe23
