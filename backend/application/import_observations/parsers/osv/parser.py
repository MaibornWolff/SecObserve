import logging
from dataclasses import dataclass
from json import dumps
from typing import Optional

from packageurl import PackageURL
from semver import Version

from application.core.models import Branch, Observation, Product
from application.import_observations.parsers.base_parser import BaseParser
from application.import_observations.services.osv_cache import get_osv_vulnerability
from application.import_observations.types import OSV_Component, Parser_Type
from application.licenses.models import License_Component

logger = logging.getLogger("secobserve.import_observations")


@dataclass
class Event:
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
            for vulnerability in osv_component.vulnerabilities:
                license_component = License_Component.objects.filter(
                    component_purl=osv_component.component_purl
                ).first()
                osv_vulnerability = get_osv_vulnerability(
                    osv_id=vulnerability.id, modified=vulnerability.modified
                )

                if osv_vulnerability is None:
                    logger.warning("OSV vulnerability %s not found", vulnerability.id)
                    continue

                if license_component is None:
                    logger.warning(
                        "Licencse component for PURL %s not found",
                        osv_component.component_purl,
                    )
                    continue

                if osv_vulnerability.get("withdrawn"):
                    continue

                vulnerability_id, vulnerability_id_aliases = self._get_osv_ids(
                    osv_vulnerability
                )
                osv_cvss3_vector, osv_cvss4_vector = self._get_cvss(osv_vulnerability)

                affected = self._get_affected(
                    osv_component.component_purl, osv_vulnerability, product, branch
                )

                component_in_versions = None
                component_in_ranges = None
                recommendation = ""

                for affected_item in affected:
                    component_in_versions = self._is_version_in_affected(
                        license_component.component_version, affected_item
                    )
                    component_in_ranges, fixed_version = self._is_version_in_ranges(
                        license_component.component_version, affected_item
                    )

                    if component_in_versions or component_in_ranges:
                        affected_cvss3_vector, affected_cvss4_vector = (
                            self._get_affected_cvss(affected_item)
                        )
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
                        ),
                        recommendation=recommendation,
                        cvss3_vector=osv_cvss3_vector,
                        cvss4_vector=osv_cvss4_vector,
                        vulnerability_id=vulnerability_id,
                        vulnerability_id_aliases=vulnerability_id_aliases,
                        origin_component_name=license_component.component_name,
                        origin_component_version=license_component.component_version,
                        origin_component_purl=license_component.component_purl,
                        origin_component_cpe=license_component.component_cpe,
                        origin_component_dependencies=license_component.component_dependencies,
                    )
                    observations.append(observation)

                    observation.unsaved_references = self._get_references(
                        osv_vulnerability
                    )

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
    ) -> str:
        osv_description_parts: list[str] = []
        if osv_vulnerability.get("summary"):
            osv_description_parts.append(str(osv_vulnerability.get("summary")))
        if osv_vulnerability.get("details"):
            osv_description_parts.append(str(osv_vulnerability.get("details")))

        if component_in_versions:
            osv_description_parts.append(
                "**Confidence: High** (Component found in affected versions)"
            )
        elif component_in_ranges:
            osv_description_parts.append(
                "**Confidence: High** (Component found in affected ranges)"
            )
        elif component_in_versions is None and component_in_ranges is None:
            osv_description_parts.append(
                "**Confidence: Low** (No information about affected versions or ranges)"
            )
        elif component_in_ranges is None:
            osv_description_parts.append(
                "**Confidence: Low** (Not all ranges could be evaluated)"
            )

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
        package_namespace = parsed_purl.namespace
        package_name = self._get_package_name(parsed_purl, package_namespace)

        package_osv_ecosystem = OSV_Non_Linux_Ecosystems.get(package_type)
        if (
            not package_osv_ecosystem
            and branch
            and branch.osv_linux_distribution
            and branch.osv_linux_release
        ):
            package_osv_ecosystem = (
                f"{branch.osv_linux_distribution}:{branch.osv_linux_release}"
            )
        if not package_osv_ecosystem and branch and branch.osv_linux_distribution:
            package_osv_ecosystem = branch.osv_linux_distribution
        if (
            not package_osv_ecosystem
            and product.osv_linux_distribution
            and product.osv_linux_release
        ):
            package_osv_ecosystem = (
                f"{product.osv_linux_distribution}:{product.osv_linux_release}"
            )
        if not package_osv_ecosystem and product.osv_linux_distribution:
            package_osv_ecosystem = product.osv_linux_distribution

        for affected_item in osv_vulnerability.get("affected", []):
            package = affected_item.get("package", {})
            affected_ecosystem = package.get("ecosystem")
            affected_name = package.get("name")
            if (
                package_osv_ecosystem == affected_ecosystem
                and package_name == affected_name
            ):
                affected.append(affected_item)

        return affected

    def _get_package_name(
        self, parsed_purl: PackageURL, package_namespace: Optional[str]
    ) -> str:
        package_name = parsed_purl.name
        if package_namespace and package_namespace not in ["alpine", "debian"]:
            if package_namespace == "maven":
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

    def _is_version_in_ranges(
        self, version: str, affected: dict
    ) -> tuple[Optional[bool], Optional[str]]:
        if not version:
            return None, None

        version_semver = self._get_semver(version)
        if not version_semver:
            return None, None

        osv_ranges = affected.get("ranges", [])

        num_ranges = len(osv_ranges)
        num_rejected_ranges = 0

        for osv_range in osv_ranges:
            if (
                osv_range.get("type") == "ECOSYSTEM"
                or osv_range.get("type") == "SEMVER"
            ):
                events = self._get_events(osv_range)
                for event in events:
                    introduced_semver = self._get_semver(event.introduced)
                    fixed_semver = self._get_semver(event.fixed)

                    if not introduced_semver:
                        introduced_semver = Version.parse("0.0.0")
                    if not fixed_semver:
                        continue

                    if introduced_semver <= version_semver < fixed_semver:
                        return True, event.fixed

                num_rejected_ranges += 1

        if num_rejected_ranges == num_ranges:
            return False, None

        return None, None

    def _get_events(self, osv_range: dict) -> list[Event]:
        events = []
        event = Event(introduced="", fixed="")
        for osv_event in osv_range.get("events", []):
            introduced = osv_event.get("introduced", "")
            if introduced:
                event.introduced = introduced
            fixed = osv_event.get("fixed", "")
            if fixed:
                event.fixed = fixed
            if event.introduced and event.fixed:
                events.append(event)
                event = Event(introduced="", fixed="")
        return events

    def _get_semver(self, version: Optional[str]) -> Optional[Version]:
        if not version:
            return None

        if version == "0":
            return Version.parse("0.0.0")

        if len(version.split("-")) == 2:
            prefix = version.split("-")[0]
            if len(prefix.split(".")) == 2:
                prefix = f"{prefix}.0"
            version = f"{prefix}-{version.split('-')[1]}"

        if len(version.split(".")) == 2:
            version = f"{version}.0"

        if not Version.is_valid(version):
            return None

        return Version.parse(version)
