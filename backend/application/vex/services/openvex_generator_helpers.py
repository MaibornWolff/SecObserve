from typing import Optional

from application.vex.types import OpenVEXVulnerability


class OpenVEXVulnerabilityCache:
    def __init__(self) -> None:
        self.vulnerabilities: dict[str, OpenVEXVulnerability] = {}

    def add_vulnerability(self, vulnerability: OpenVEXVulnerability) -> None:
        if not self.vulnerabilities.get(vulnerability.name):
            self.vulnerabilities[vulnerability.name] = vulnerability

    def get_vulnerability(self, name: str) -> Optional[OpenVEXVulnerability]:
        return self.vulnerabilities.get(name)
