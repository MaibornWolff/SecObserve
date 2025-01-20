from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class OSV_Vulnerability:
    id: str
    modified: datetime


@dataclass
class OSV_Component:
    id: int
    component_purl: str
    vulnerabilities: set[OSV_Vulnerability]
