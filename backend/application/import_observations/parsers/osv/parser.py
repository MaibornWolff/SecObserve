import logging
from dataclasses import dataclass
from datetime import datetime
from json import dumps
from typing import Optional

from packageurl import PackageURL

from application.core.models import Branch, Observation, Product
from application.import_observations.parsers.base_parser import BaseParser
from application.import_observations.services.osv_cache import get_osv_vulnerability
from application.import_observations.types import ExtendedSemVer, Parser_Type
from application.licenses.models import License_Component

logger = logging.getLogger("secobserve.import_observations")


@dataclass(frozen=True)
class OSV_Vulnerability:
    id: str
    modified: datetime


@dataclass
class OSV_Component:
    license_component: License_Component
    vulnerabilities: set[OSV_Vulnerability]


@dataclass
class Event:
    type: str
    introduced: str
    fixed: str


OSV_Non_Linux_Ecosystems = {
    "bitnami": "Bitnami",
    "conan": "ConanCenter",
    "cran": "CRAN",
    "cargo": "crates.io",
    "golang": "Go",
    "hackage": "Hackage",
    "hex": "Hex",
    "maven": "Maven",
    "npm": "npm",
    "nuget": "NuGet",
    "pub": "Pub",
    "pypi": "PyPI",
    "gem": "RubyGems",
    "swift": "SwiftURL",
}


class OSVParser(BaseParser):
    @classmethod
    def get_name(cls) -> str:
        return "OSV (Open Source Vulnerabilities)"

    @classmethod
    def get_type(cls) -> str:
        return Parser_Type.TYPE_SCA

    def get_observations(  # pylint: disable=too-many-locals
        self, data: list[OSV_Component], product: Product, branch: Optional[Branch]
    ) -> list[Observation]:
        observations = []

        for osv_component in data:
            ordered_vulnerabilities = sorted(osv_component.vulnerabilities, key=lambda x: x.id)

            for vulnerability in ordered_vulnerabilities:
                osv_vulnerability = get_osv_vulnerability(osv_id=vulnerability.id, modified=vulnerability.modified)

                if osv_vulnerability is None:
                    logger.warning("OSV vulnerability %s not found", vulnerability.id)
                    continue

                if osv_vulnerability.get("withdrawn"):
                    continue

                vulnerability_id, vulnerability_id_aliases = self._get_osv_ids(osv_vulnerability)
                osv_cvss3_vector, osv_cvss4_vector = self._get_cvss(osv_vulnerability)

                affected = self._get_affected(
                    osv_component.license_component.component_purl,
                    osv_vulnerability,
                    product,
                    branch,
                )

                component_in_versions = None
                component_in_ranges = None
                recommendation = ""
                events = []

                for affected_item in affected:
                    component_in_versions = self._is_version_in_affected(
                        osv_component.license_component.component_version, affected_item
                    )
                    component_in_ranges, fixed_version, affected_events = self._is_version_in_ranges(
                        osv_component.license_component.component_version,
                        affected_item,
                    )

                    events.extend(affected_events)

                    if component_in_versions or component_in_ranges:
                        affected_cvss3_vector, affected_cvss4_vector = self._get_affected_cvss(affected_item)
                        if affected_cvss3_vector:
                            osv_cvss3_vector = affected_cvss3_vector
                        if affected_cvss4_vector:
                            osv_cvss4_vector = affected_cvss4_vector

                        if fixed_version:
                            recommendation = f"Update to version {fixed_version}"

                        break

                if (
                    (component_in_versions is None and component_in_ranges is None)
                    or component_in_versions is True
                    or component_in_ranges is not False
                ):
                    observation = Observation(
                        title=vulnerability_id,
                        description=self._get_description(
                            osv_vulnerability,
                            component_in_versions,
                            component_in_ranges,
                            events,
                        ),
                        recommendation=recommendation,
                        cvss3_vector=osv_cvss3_vector,
                        cvss4_vector=osv_cvss4_vector,
                        vulnerability_id=vulnerability_id,
                        vulnerability_id_aliases=vulnerability_id_aliases,
                        origin_component_name=osv_component.license_component.component_name,
                        origin_component_version=osv_component.license_component.component_version,
                        origin_component_purl=osv_component.license_component.component_purl,
                        origin_component_cpe=osv_component.license_component.component_cpe,
                        origin_component_dependencies=osv_component.license_component.component_dependencies,
                    )
                    observations.append(observation)

                    observation.unsaved_references = self._get_references(osv_vulnerability)

                    evidence = []
                    evidence.append("OSV Vulnerability")
                    evidence.append(dumps(osv_vulnerability))
                    observation.unsaved_evidences.append(evidence)

        return observations

    def _get_osv_ids(self, osv_vulnerability: dict) -> tuple[str, str]:
        osv_id = str(osv_vulnerability.get("id", ""))

        aliases: list[str] = []
        for alias in osv_vulnerability.get("aliases", []):
            if not osv_id.startswith("CVE-") and str(alias).startswith("CVE-"):
                aliases.append(str(osv_id))
                osv_id = str(alias)
            elif str(alias) != osv_id:
                aliases.append(str(alias))

        aliases.sort()
        return osv_id, ", ".join(aliases)

    def _get_description(
        self,
        osv_vulnerability: dict,
        component_in_versions: Optional[bool],
        component_in_ranges: Optional[bool],
        events: list[Event],
    ) -> str:
        osv_description_parts: list[str] = []
        if osv_vulnerability.get("summary"):
            osv_description_parts.append(str(osv_vulnerability.get("summary")))
        if osv_vulnerability.get("details"):
            osv_description_parts.append(str(osv_vulnerability.get("details")))

        if component_in_versions:
            osv_description_parts.append("**Confidence: High** (Component found in affected versions)")
        elif component_in_ranges:
            osv_description_parts.append("**Confidence: High** (Component found in affected ranges)")
        elif component_in_versions is None and component_in_ranges is None:
            osv_description_parts.append("**Confidence: Low** (No information about affected versions or ranges)")
        elif component_in_ranges is None:
            osv_description_parts.append("**Confidence: Low** (Events could not be evaluated)")
            osv_description_parts.append("**Events:**")
            for event in events:
                osv_description_parts.append(f"* {event.type}: Introduced: {event.introduced} - Fixed: {event.fixed}")

        return "\n\n".join(osv_description_parts)

    def _get_cvss(self, osv_vulnerability: dict) -> tuple[str, str]:
        cvss3_vector = ""
        cvss4_vector = ""

        severities = osv_vulnerability.get("severity", [])
        for severity in severities:
            if severity.get("type") == "CVSS_V3":
                cvss3_vector = severity.get("score")
            if severity.get("type") == "CVSS_V4":
                cvss4_vector = severity.get("score")

        return cvss3_vector, cvss4_vector

    def _get_references(self, osv_vulnerability: dict) -> list[str]:
        references = []
        for reference in osv_vulnerability.get("references", []):
            references.append(reference.get("url"))
        return references

    def _get_affected(
        self,
        purl: str,
        osv_vulnerability: dict,
        product: Product,
        branch: Optional[Branch],
    ) -> list[dict]:
        try:
            parsed_purl = PackageURL.from_string(purl)
        except ValueError as e:
            logger.error("Invalid PURL %s: %s", purl, str(e))
            return []

        affected = []

        package_type = parsed_purl.type
        package_name = self._get_package_name(parsed_purl)

        package_osv_ecosystem = OSV_Non_Linux_Ecosystems.get(package_type)

        if not package_osv_ecosystem and branch and branch.osv_linux_distribution and branch.osv_linux_release:
            package_osv_ecosystem = f"{branch.osv_linux_distribution}:{branch.osv_linux_release}"
        if not package_osv_ecosystem and branch and branch.osv_linux_distribution:
            package_osv_ecosystem = branch.osv_linux_distribution

        if not package_osv_ecosystem and product.osv_linux_distribution and product.osv_linux_release:
            package_osv_ecosystem = f"{product.osv_linux_distribution}:{product.osv_linux_release}"
        if not package_osv_ecosystem and product.osv_linux_distribution:
            package_osv_ecosystem = product.osv_linux_distribution

        package_osv_ecosystem = self._get_linux_package_osv_ecosystem(parsed_purl, package_osv_ecosystem)

        for affected_item in osv_vulnerability.get("affected", []):
            package = affected_item.get("package", {})
            affected_ecosystem = package.get("ecosystem")
            affected_name = package.get("name")
            if package_osv_ecosystem == affected_ecosystem and package_name == affected_name:
                affected.append(affected_item)

        return affected

    def _get_linux_package_osv_ecosystem(
        self, parsed_purl: PackageURL, package_osv_ecosystem: Optional[str]
    ) -> Optional[str]:
        package_type = parsed_purl.type
        if not package_osv_ecosystem and parsed_purl.qualifiers and isinstance(parsed_purl.qualifiers, dict):
            if package_type == "apk":
                distro_name = parsed_purl.qualifiers.get("distro_name")
                if distro_name and distro_name.startswith("alpine-"):
                    package_osv_ecosystem = f"Alpine:v{distro_name[7:]}"
            elif package_type == "deb" and parsed_purl.namespace == "ubuntu":
                distro = parsed_purl.qualifiers.get("distro")
                if distro and distro.startswith("ubuntu-"):
                    distro_version = distro[7:]
                    distro_version_parts = distro_version.split(".")
                    if (
                        len(distro_version_parts) == 2
                        and distro_version_parts[0].isdigit()
                        and int(distro_version_parts[0]) % 2 == 0
                        and distro_version_parts[1] == "04"
                    ):
                        distro_version = f"{distro_version}:LTS"
                    package_osv_ecosystem = f"Ubuntu:{distro_version}"
        return package_osv_ecosystem

    def _get_package_name(self, parsed_purl: PackageURL) -> str:
        package_name = parsed_purl.name
        package_namespace = parsed_purl.namespace
        package_type = parsed_purl.type
        if package_namespace and OSV_Non_Linux_Ecosystems.get(package_type):
            if package_type == "maven":
                package_name = f"{package_namespace}:{package_name}"
            else:
                package_name = f"{package_namespace}/{package_name}"
        return package_name

    def _get_affected_cvss(self, affected: dict) -> tuple[str, str]:
        cvss3_vector = ""
        cvss4_vector = ""

        severity = affected.get("severity")
        if severity:
            if severity.get("type") == "CVSS_V3":
                cvss3_vector = severity.get("score")
            if severity.get("type") == "CVSS_V4":
                cvss4_vector = severity.get("score")

        return cvss3_vector, cvss4_vector

    def _is_version_in_affected(self, version: str, affected: dict) -> bool:
        if not version:
            return True

        versions = affected.get("versions", [])
        return version in versions

    def _is_version_in_ranges(self, version: str, affected: dict) -> tuple[Optional[bool], Optional[str], list[Event]]:
        if not version:
            return None, None, []

        events = self._get_events(affected)

        version_semver = ExtendedSemVer.parse(version)
        if not version_semver:
            return None, None, events

        num_rejected_events = 0
        for event in events:
            if event.type in ("ECOSYSTEM", "SEMVER"):
                introduced_semver = ExtendedSemVer.parse(event.introduced)
                fixed_semver = ExtendedSemVer.parse(event.fixed)

                if not introduced_semver:
                    introduced_semver = ExtendedSemVer.parse("0.0.0")
                if not fixed_semver:
                    continue

                if introduced_semver <= version_semver < fixed_semver:
                    return True, event.fixed, events

                num_rejected_events += 1

        if num_rejected_events == len(events):
            return False, None, events

        return None, None, events

    def _get_events(self, affected: dict) -> list[Event]:
        events = []

        osv_ranges = affected.get("ranges", [])
        for osv_range in osv_ranges:
            event = Event(osv_range.get("type", ""), introduced="", fixed="")
            for osv_event in osv_range.get("events", []):
                introduced = osv_event.get("introduced", "")
                if introduced:
                    event.introduced = introduced
                fixed = osv_event.get("fixed", "")
                if fixed:
                    event.fixed = fixed
                if event.introduced and event.fixed:
                    events.append(event)
                    event = Event(osv_range.get("type", ""), introduced="", fixed="")
        return events
