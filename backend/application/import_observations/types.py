from dataclasses import dataclass
from datetime import datetime


class Parser_Source:
    SOURCE_API = "API"
    SOURCE_FILE = "File"
    SOURCE_MANUAL = "Manual"
    SOURCE_OTHER = "Other"
    SOURCE_UNKNOWN = "Unknown"

    SOURCE_CHOICES = [
        (SOURCE_API, SOURCE_API),
        (SOURCE_FILE, SOURCE_FILE),
        (SOURCE_MANUAL, SOURCE_MANUAL),
        (SOURCE_OTHER, SOURCE_OTHER),
        (SOURCE_UNKNOWN, SOURCE_UNKNOWN),
    ]


class Parser_Type:
    TYPE_SCA = "SCA"
    TYPE_SAST = "SAST"
    TYPE_DAST = "DAST"
    TYPE_IAST = "IAST"
    TYPE_SECRETS = "Secrets"
    TYPE_INFRASTRUCTURE = "Infrastructure"
    TYPE_OTHER = "Other"
    TYPE_MANUAL = "Manual"

    TYPE_CHOICES = [
        (TYPE_SCA, TYPE_SCA),
        (TYPE_SAST, TYPE_SAST),
        (TYPE_DAST, TYPE_DAST),
        (TYPE_IAST, TYPE_IAST),
        (TYPE_SECRETS, TYPE_SECRETS),
        (TYPE_INFRASTRUCTURE, TYPE_INFRASTRUCTURE),
        (TYPE_OTHER, TYPE_OTHER),
        (TYPE_MANUAL, TYPE_MANUAL),
    ]


class Parser_Filetype:
    FILETYPE_CSV = "CSV"
    FILETYPE_JSON = "JSON"


@dataclass(frozen=True)
class OSV_Vulnerability:
    id: str
    modified: datetime


@dataclass
class OSV_Component:
    id: int
    component_purl: str
    vulnerabilities: set[OSV_Vulnerability]
