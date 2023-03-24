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
    "brainpoolP256r1tls13",
    "brainpoolP384r1tls13",
    "brainpoolP512r1tls13",
    "brainpoolP256r1",
    "brainpoolP384r1",
    "brainpoolP512r1",
    "secp256r1",
    "prime256v1",  # equivalent to secp256r1 according to RFC 4492
    "secp384r1",
    "secp521r1",
    "ffdhe3072",
    "ffdhe4096",
]

RECOMMENDED_SIGNATURE_ALGORITHMS = [
    "rsa_sha256",
    "rsa_sha384",
    "rsa_sha512",
    "dsa_sha256",
    "dsa_sha384",
    "dsa_sha512",
    "ecdsa_sha256",
    "ecdsa_sha384",
    "ecdsa_sha512",
    "rsa_pss_rsae_sha256",
    "rsa_pss_rsae_sha384",
    "rsa_pss_rsae_sha512",
    "rsa_pss_pss_sha256",
    "rsa_pss_pss_sha384",
    "rsa_pss_pss_sha512",
    "ecdsa_secp256r1_sha256",
    "ecdsa_secp384r1_sha384",
    "ecdsa_secp521r1_sha512",
    "ecdsa_brainpoolP256r1tls13_sha256",
    "ecdsa_brainpoolP384r1tls13_sha384",
    "ecdsa_brainpoolP512r1tls13_sha512",
]

BSI_LINK = "https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TG02102/BSI-TR-02102-2.pdf?__blob=publicationFile&v=5"  # noqa: E501


class CryptoLyzerParser(BaseParser, BaseFileParser):
    @classmethod
    def get_name(cls) -> str:
        return "CryptoLyzer"

    @classmethod
    def get_type(cls) -> str:
        return Parser.TYPE_DAST

    def check_format(self, file: File) -> tuple[bool, list[str], dict]:
        try:
            data = load(file)
        except Exception:
            return False, ["File is not valid JSON"], None

        if (
            not data.get("target")
            or not data.get("versions")
            or not data.get("ciphers")
            or not data.get("curves")
        ):
            return False, ["File is not a valid CryptoLyzer format"], None

        return True, [], data

    def get_observations(self, data: dict) -> list[Observation]:
        observations = []

        observation = self.check_weak_protocols(data)
        if observation:
            observations.append(observation)

        observation = self.check_ciphers(
            "tls1_2", "TLS 1.2", TLS12_RECOMMENDED_CIPHERS, data
        )
        if observation:
            observations.append(observation)
        observation = self.check_ciphers(
            "tls1_3", "TLS 1.3", TLS13_RECOMMENDED_CIPHERS, data
        )
        if observation:
            observations.append(observation)

        observation = self.check_curves(data)
        if observation:
            observations.append(observation)

        observation = self.check_signature_algorithms(data)
        if observation:
            observations.append(observation)

        return observations

    def check_weak_protocols(self, data: dict) -> Observation | None:
        endpoint_url = self.get_endpoint_url(data.get("versions", {}).get("target", {}))
        versions = data.get("versions", {}).get("versions", []).copy()
        if "tls1_2" in versions:
            versions.remove("tls1_2")
        if "tls1_3" in versions:
            versions.remove("tls1_3")
        description = (
            "**Weak protocols according to BSI recommendations:**\n* "
            + "\n* ".join(versions)
        )
        if versions:
            observation = Observation(
                title="Weak protocols detected",
                description=description,
                parser_severity=Observation.SEVERITY_HIGH,
                origin_endpoint_url=endpoint_url,
                scanner=self.get_name(),
            )

            observation.unsaved_references = [BSI_LINK]

            evidence = []
            evidence.append("Result")
            evidence.append(dumps(data.get("versions")))
            observation.unsaved_evidences.append(evidence)

            return observation
        else:
            return None

    def check_ciphers(
        self,
        protocol: str,
        protocol_name: str,
        recommended_cipher_suites: list[str],
        data: dict,
    ) -> Observation | None:
        ciphers = data.get("ciphers", [])
        for cipher in ciphers:
            cipher_protocol = cipher.get("target", {}).get("proto_version")
            if protocol == cipher_protocol:
                unrecommended_cipher_suites = []
                cipher_suites = cipher.get("cipher_suites", {})
                for cipher_suite in cipher_suites:
                    keys = cipher_suite.keys()
                    for key in keys:
                        if key not in recommended_cipher_suites:
                            unrecommended_cipher_suites.append(key)

                if unrecommended_cipher_suites:
                    endpoint_url = self.get_endpoint_url(cipher.get("target", {}))
                    description = (
                        "**Unrecommended cipher suites according to BSI recommendations:**\n* "
                        + "\n* ".join(unrecommended_cipher_suites)
                    )
                    observation = Observation(
                        title="Unrecommended " + protocol_name + " cipher suites",
                        description=description,
                        parser_severity=Observation.SEVERITY_MEDIUM,
                        origin_endpoint_url=endpoint_url,
                        scanner=self.get_name(),
                    )

                    evidence = []
                    evidence.append("Result")
                    evidence.append(dumps(cipher))
                    observation.unsaved_evidences.append(evidence)

                    observation.unsaved_references = [BSI_LINK]

                    return observation

        return None

    def check_curves(
        self,
        data: dict,
    ) -> Observation | None:
        curves = data.get("curves", {})
        unrecommended_curves = []
        inner_curves = curves.get("curves", {})
        for inner_curve in inner_curves:
            keys = inner_curve.keys()
            for key in keys:
                if key.lower() not in RECOMMENDED_ELLIPTIC_CURVES:
                    unrecommended_curves.append(key)

        if unrecommended_curves:
            endpoint_url = self.get_endpoint_url(curves.get("target", {}))
            description = (
                "**Unrecommended elliptic curves according to BSI recommendations:**\n* "
                + "\n* ".join(unrecommended_curves)
            )
            observation = Observation(
                title="Unrecommended elliptic curves",
                description=description,
                parser_severity=Observation.SEVERITY_MEDIUM,
                origin_endpoint_url=endpoint_url,
                scanner=self.get_name(),
            )

            evidence = []
            evidence.append("Result")
            evidence.append(dumps(curves))
            observation.unsaved_evidences.append(evidence)

            observation.unsaved_references = [BSI_LINK]

            return observation
        else:
            return None

    def check_signature_algorithms(
        self,
        data: dict,
    ) -> Observation | None:
        signature_algorithms = data.get("sigalgos", {})
        unrecommended_signature_algorithms = []
        inner_signature_algorithms = signature_algorithms.get("sig_algos", {})
        for inner_signature_algorithm in inner_signature_algorithms:
            keys = inner_signature_algorithm.keys()
            for key in keys:
                if key.lower() not in RECOMMENDED_SIGNATURE_ALGORITHMS:
                    unrecommended_signature_algorithms.append(key)

        if unrecommended_signature_algorithms:
            endpoint_url = self.get_endpoint_url(signature_algorithms.get("target", {}))
            description = (
                "**Unrecommended signature algorithms according to BSI recommendations:**\n* "
                + "\n* ".join(unrecommended_signature_algorithms)
            )
            observation = Observation(
                title="Unrecommended signature algorithms",
                description=description,
                parser_severity=Observation.SEVERITY_MEDIUM,
                origin_endpoint_url=endpoint_url,
                scanner=self.get_name(),
            )

            evidence = []
            evidence.append("Result")
            evidence.append(dumps(signature_algorithms))
            observation.unsaved_evidences.append(evidence)

            observation.unsaved_references = [BSI_LINK]

            return observation
        else:
            return None

    def get_endpoint_url(self, target: dict) -> str | None:
        hostname = target.get("address")
        port = target.get("port")
        endpoint_url = None
        if hostname:
            endpoint_url = "https://" + hostname
            if port:
                endpoint_url += ":" + str(port)
        return endpoint_url
