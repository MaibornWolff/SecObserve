from json import load, dumps
from django.core.files.base import File

from application.core.models import Observation, Parser
from application.import_observations.parsers.base_parser import (
    BaseParser,
    BaseFileParser,
)

# Recommended cipher suites according to German BSI as of 2020
TLS12_RECOMMENDED_CIPHERS = [
    "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256",
    "TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384",
    "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
    "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
    "TLS_ECDHE_ECDSA_WITH_AES_128_CCM",
    "TLS_ECDHE_ECDSA_WITH_AES_256_CCM",
    "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256",
    "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384",
    "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
    "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
    "TLS_DHE_DSS_WITH_AES_128_CBC_SHA256",
    "TLS_DHE_DSS_WITH_AES_256_CBC_",
    "TLS_DHE_DSS_WITH_AES_128_GCM_SHA256",
    "TLS_DHE_DSS_WITH_AES_256_GCM_SHA384",
    "TLS_DHE_RSA_WITH_AES_128_CBC_SHA256",
    "TLS_DHE_RSA_WITH_AES_256_CBC_SHA256",
    "TLS_DHE_RSA_WITH_AES_128_GCM_SHA256",
    "TLS_DHE_RSA_WITH_AES_256_GCM_SHA384",
    "TLS_DHE_RSA_WITH_AES_128_CCM",
    "TLS_DHE_RSA_WITH_AES_256_CCM",
    "TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA256",
    "TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA384",
    "TLS_ECDH_ECDSA_WITH_AES_128_GCM_SHA256",
    "TLS_ECDH_ECDSA_WITH_AES_256_GCM_SHA384",
    "TLS_ECDH_RSA_WITH_AES_128_CBC_SHA256",
    "TLS_ECDH_RSA_WITH_AES_256_CBC_SHA384",
    "TLS_ECDH_RSA_WITH_AES_128_GCM_SHA256",
    "TLS_ECDH_RSA_WITH_AES_256_GCM_SHA384",
    "TLS_DH_DSS_WITH_AES_128_CBC_SHA256",
    "TLS_DH_DSS_WITH_AES_256_CBC_SHA256",
    "TLS_DH_DSS_WITH_AES_128_GCM_SHA256",
    "TLS_DH_DSS_WITH_AES_256_GCM_SHA384",
    "TLS_DH_RSA_WITH_AES_128_CBC_SHA256",
    "TLS_DH_RSA_WITH_AES_256_CBC_SHA256",
    "TLS_DH_RSA_WITH_AES_128_GCM_SHA256",
    "TLS_DH_RSA_WITH_AES_256_GCM_SHA384",
    "TLS_ECDHE_PSK_WITH_AES_128_CBC_SHA256",
    "TLS_ECDHE_PSK_WITH_AES_256_CBC_SHA384",
    "TLS_ECDHE_PSK_WITH_AES_128_GCM_SHA256",
    "TLS_ECDHE_PSK_WITH_AES_256_GCM_SHA384",
    "TLS_ECDHE_PSK_WITH_AES_128_CCM_SHA256",
    "TLS_DHE_PSK_WITH_AES_128_CBC_SHA256",
    "TLS_DHE_PSK_WITH_AES_256_CBC_SHA384",
    "TLS_DHE_PSK_WITH_AES_128_GCM_SHA256",
    "TLS_DHE_PSK_WITH_AES_256_GCM_SHA384",
    "TLS_DHE_PSK_WITH_AES_128_CCM",
    "TLS_DHE_PSK_WITH_AES_256_CCM",
    "TLS_RSA_PSK_WITH_AES_128_CBC_SHA256",
    "TLS_RSA_PSK_WITH_AES_256_CBC_SHA384",
    "TLS_RSA_PSK_WITH_AES_128_GCM_SHA256",
    "TLS_RSA_PSK_WITH_AES_256_GCM_SHA384",
]

TLS13_RECOMMENDED_CIPHERS = [
    "TLS_AES_128_GCM_SHA256",
    "TLS_AES_256_GCM_SHA384",
    "TLS_AES_128_CCM_SHA256",
]

RECOMMENDED_ELLIPTIC_CURVES = [
    "brainpoolP256r1",
    "brainpoolP384r1",
    "brainpoolP512r1",
    "secp256r1",
    "prime256v1",  # equivalent to secp256r1 according to RFC 4492
    "secp384r1",
    "secp521r1",
]

BSI_LINK = "https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Publikationen/TechnischeRichtlinien/TR02102/BSI-TR-02102-2.pdf?__blob=publicationFile&v=4"  # noqa: E501


class SSLyzeParser(BaseParser, BaseFileParser):
    @classmethod
    def get_name(cls) -> str:
        return "SSLyze"

    @classmethod
    def get_type(cls) -> str:
        return Parser.TYPE_DAST

    def check_format(self, file: File) -> tuple[bool, list[str], dict]:
        try:
            data = load(file)
        except Exception:
            return False, ["File is not valid JSON"], None

        if not data.get("sslyze_url"):
            return False, ["File is not a valid SSLyze format"], None

        return True, [], data

    def get_observations(self, data: dict) -> list[Observation]:
        observations = []

        scanner = self.get_scanner(data)
        server_scan_results = data.get("server_scan_results", [])
        for server_scan_result in server_scan_results:
            endpoint_url = self.get_endpoint_url(server_scan_result)

            scan_status = server_scan_result.get("scan_status", "Unkown status")
            if scan_status != "COMPLETED":
                observation = Observation(
                    title=scan_status,
                    parser_severity=Observation.SEVERITY_HIGH,
                    origin_endpoint_url=endpoint_url,
                    scanner=scanner,
                )

                evidence = []
                evidence.append("Result")
                evidence.append(dumps(server_scan_result))
                observation.unsaved_evidences.append(evidence)

                observations.append(observation)

                continue

            scan_result = server_scan_result.get("scan_result")
            if scan_result:
                observations += self.get_certificate_observations(
                    scan_result.get("certificate_info", {}),
                    endpoint_url,
                    scanner,
                )

                observations.append(
                    self.get_weak_protocol(
                        scan_result.get("ssl_2_0_cipher_suites", {}),
                        "SSL 2.0",
                        endpoint_url,
                        scanner,
                    )
                )
                observations.append(
                    self.get_weak_protocol(
                        scan_result.get("ssl_3_0_cipher_suites", {}),
                        "SSL 3.0",
                        endpoint_url,
                        scanner,
                    )
                )
                observations.append(
                    self.get_weak_protocol(
                        scan_result.get("tls_1_0_cipher_suites", {}),
                        "TLS 1.0",
                        endpoint_url,
                        scanner,
                    )
                )
                observations.append(
                    self.get_weak_protocol(
                        scan_result.get("tls_1_1_cipher_suites", {}),
                        "TLS 1.1",
                        endpoint_url,
                        scanner,
                    )
                )

                observations.append(
                    self.get_strong_protocol(
                        scan_result.get("tls_1_2_cipher_suites", {}),
                        "TLS 1.2",
                        TLS12_RECOMMENDED_CIPHERS,
                        endpoint_url,
                        scanner,
                    )
                )
                observations.append(
                    self.get_strong_protocol(
                        scan_result.get("tls_1_3_cipher_suites", {}),
                        "TLS 1.3",
                        TLS13_RECOMMENDED_CIPHERS,
                        endpoint_url,
                        scanner,
                    )
                )

                observations.append(
                    self.get_elliptic_curves(
                        scan_result.get("elliptic_curves", {}),
                        endpoint_url,
                        scanner,
                    )
                )

                observations.append(
                    self.get_heartbleed(
                        scan_result.get("heartbleed", {}),
                        endpoint_url,
                        scanner,
                    )
                )
                observations.append(
                    self.get_ccs_injection(
                        scan_result.get("openssl_ccs_injection", {}),
                        endpoint_url,
                        scanner,
                    )
                )

                observations.append(
                    self.get_session_renegotiation(
                        scan_result.get("session_renegotiation", {}),
                        endpoint_url,
                        scanner,
                    )
                )

        observations_without_none = [i for i in observations if i is not None]

        return observations_without_none

    def get_endpoint_url(self, server_scan_result: dict) -> str:
        server_location = server_scan_result.get("server_location", {})
        hostname = server_location.get("hostname")
        port = server_location.get("port")
        if hostname:
            endpoint_url = "https://" + hostname
            if port:
                endpoint_url += ":" + str(port)
            return endpoint_url
        return None

    def get_scanner(self, data: dict) -> str:
        scanner = "SSLyze"
        version = data.get("sslyze_version")
        if version:
            scanner += " / " + version
        return scanner

    def get_certificate_observations(
        self, certificate_info: dict, endpoint_url: str, scanner: str
    ) -> list[Observation]:
        observations = []

        if certificate_info.get("status") == "COMPLETED":
            certificate_deployments = certificate_info.get("result", {}).get(
                "certificate_deployments", []
            )
            for certificate_deployment in certificate_deployments:
                if not certificate_deployment.get(
                    "leaf_certificate_subject_matches_hostname", True
                ):
                    observation = Observation(
                        title="Leaf certificate subject does not match hostname",
                        parser_severity=Observation.SEVERITY_HIGH,
                        origin_endpoint_url=endpoint_url,
                        scanner=scanner,
                    )

                    evidence = []
                    evidence.append("Result")
                    evidence.append(dumps(certificate_deployment))
                    observation.unsaved_evidences.append(evidence)

                    observations.append(observation)

                path_validation_results = certificate_deployment.get(
                    "path_validation_results", []
                )
                openssl_errors = {}
                for path_validation_result in path_validation_results:
                    openssl_error_string = path_validation_result.get(
                        "openssl_error_string"
                    )
                    if openssl_error_string:
                        name = path_validation_result.get("trust_store", {}).get(
                            "name", ""
                        )
                        version = path_validation_result.get("trust_store", {}).get(
                            "version", ""
                        )
                        name_version = name + " / " + version
                        openssl_error = openssl_errors.get(openssl_error_string)
                        if openssl_error:
                            openssl_error = openssl_error.append(name_version)
                        else:
                            openssl_errors[openssl_error_string] = [name_version]

                for openssl_error in openssl_errors:
                    description = "**Truststores:**\n* " + "\n* ".join(
                        openssl_errors[openssl_error]
                    )

                    observation = Observation(
                        title=openssl_error.capitalize(),
                        description=description,
                        parser_severity=Observation.SEVERITY_HIGH,
                        origin_endpoint_url=endpoint_url,
                        scanner=scanner,
                    )

                    evidence = []
                    evidence.append("Result")
                    evidence.append(dumps(path_validation_result))
                    observation.unsaved_evidences.append(evidence)

                    observations.append(observation)

        return observations

    def get_weak_protocol(
        self, weak_node: dict, name: str, endpoint_url: str, scanner: str
    ) -> Observation:
        if weak_node.get("status") != "COMPLETED":
            return None

        accepted_cipher_suites = weak_node.get("result", {}).get(
            "accepted_cipher_suites", []
        )
        if accepted_cipher_suites:
            observation = Observation(
                title=name + " protocol is outdated",
                parser_severity=Observation.SEVERITY_HIGH,
                origin_endpoint_url=endpoint_url,
                scanner=scanner,
            )

            evidence = []
            evidence.append("Result")
            evidence.append(dumps(weak_node))
            observation.unsaved_evidences.append(evidence)

            observation.unsaved_references = [BSI_LINK]

            return observation

        return None

    def get_strong_protocol(
        self,
        strong_node: dict,
        name: str,
        recommended_cipher_suites: list[str],
        endpoint_url: str,
        scanner: str,
    ) -> Observation:
        if strong_node.get("status") != "COMPLETED":
            return None

        unrecommended_cipher_suites = []

        accepted_cipher_suites = strong_node.get("result", {}).get(
            "accepted_cipher_suites", []
        )
        for accepted_cipher_suite in accepted_cipher_suites:
            cipher_suite_name = accepted_cipher_suite.get("cipher_suite", {}).get(
                "name"
            )
            if cipher_suite_name not in recommended_cipher_suites:
                unrecommended_cipher_suites.append(cipher_suite_name)

        if unrecommended_cipher_suites:
            description = (
                "**Unrecommended cipher suites according to BSI recommendations:**\n* "
                + "\n* ".join(unrecommended_cipher_suites)
            )
            observation = Observation(
                title="Unrecommended " + name + " cipher suites",
                description=description,
                parser_severity=Observation.SEVERITY_MEDIUM,
                origin_endpoint_url=endpoint_url,
                scanner=scanner,
            )

            evidence = []
            evidence.append("Result")
            evidence.append(dumps(strong_node))
            observation.unsaved_evidences.append(evidence)

            observation.unsaved_references = [BSI_LINK]

            return observation

        return None

    def get_elliptic_curves(
        self, elliptic_curves_node: dict, endpoint_url: str, scanner: str
    ) -> Observation:
        if elliptic_curves_node.get("status") != "COMPLETED":
            return None

        unrecommended_elliptic_curves = []

        supported_curves = elliptic_curves_node.get("result", {}).get(
            "supported_curves", []
        )
        for supported_curve in supported_curves:
            elliptic_curve_name = supported_curve.get("name")
            if elliptic_curve_name not in RECOMMENDED_ELLIPTIC_CURVES:
                unrecommended_elliptic_curves.append(elliptic_curve_name)

        if unrecommended_elliptic_curves:
            description = (
                "**Unrecommended elliptic curves according to BSI recommendations:**\n* "
                + "\n* ".join(unrecommended_elliptic_curves)
            )
            observation = Observation(
                title="Unrecommended elliptic curves",
                description=description,
                parser_severity=Observation.SEVERITY_MEDIUM,
                origin_endpoint_url=endpoint_url,
                scanner=scanner,
            )

            evidence = []
            evidence.append("Result")
            evidence.append(dumps(elliptic_curves_node))
            observation.unsaved_evidences.append(evidence)

            observation.unsaved_references = [BSI_LINK]

            return observation

        return None

    def get_heartbleed(
        self, heartbleed_node: dict, endpoint_url: str, scanner: str
    ) -> Observation:
        if heartbleed_node.get("status") != "COMPLETED":
            return None

        if heartbleed_node.get("result", {}).get("is_vulnerable_to_heartbleed", False):
            observation = Observation(
                title="Vulnerable to Heartbleed",
                parser_severity=Observation.SEVERITY_HIGH,
                origin_endpoint_url=endpoint_url,
                scanner=scanner,
            )

            evidence = []
            evidence.append("Result")
            evidence.append(dumps(heartbleed_node))
            observation.unsaved_evidences.append(evidence)

            return observation

    def get_ccs_injection(
        self, ccs_injection_node: dict, endpoint_url: str, scanner: str
    ) -> Observation:
        if ccs_injection_node.get("status") != "COMPLETED":
            return None

        if ccs_injection_node.get("result", {}).get(
            "is_vulnerable_to_ccs_injection", False
        ):
            observation = Observation(
                title="Vulnerable to CCS Injection",
                parser_severity=Observation.SEVERITY_HIGH,
                origin_endpoint_url=endpoint_url,
                scanner=scanner,
            )

            evidence = []
            evidence.append("Result")
            evidence.append(dumps(ccs_injection_node))
            observation.unsaved_evidences.append(evidence)

            return observation

    def get_session_renegotiation(
        self, session_renegotiation_node: dict, endpoint_url: str, scanner: str
    ) -> Observation:
        if session_renegotiation_node.get("status") != "COMPLETED":
            return None

        if session_renegotiation_node.get("result", {}).get(
            "is_vulnerable_to_client_renegotiation_dos", False
        ):
            observation = Observation(
                title="Vulnerable to session renegotiation DoS",
                parser_severity=Observation.SEVERITY_HIGH,
                origin_endpoint_url=endpoint_url,
                scanner=scanner,
            )

            evidence = []
            evidence.append("Result")
            evidence.append(dumps(session_renegotiation_node))
            observation.unsaved_evidences.append(evidence)

            return observation
