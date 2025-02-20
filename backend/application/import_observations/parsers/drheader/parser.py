from json import dumps
from typing import Any, Optional

from application.core.models import Branch, Observation, Product
from application.core.types import Severity
from application.import_observations.parsers.base_parser import (
    BaseFileParser,
    BaseParser,
)
from application.import_observations.types import Parser_Filetype, Parser_Type

REFERENCES = {
    "Access-Control-Allow-Origin": [
        "https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html#access-control-allow-origin",
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin",
    ],
    "Cache-Control": [
        "https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html#security-headers",
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control",
    ],
    "Content-Security-Policy": [
        "https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html",
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP",
        "https://scotthelme.co.uk/content-security-policy-an-introduction/",
        "https://scotthelme.co.uk/csp-cheat-sheet/",
    ],
    "Cross-Origin-Embedder-Policy": [
        "https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html#cross-origin-embedder-policy",
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Embedder-Policy",
        "https://scotthelme.co.uk/coop-and-coep/",
    ],
    "Cross-Origin-Opener-Policy": [
        "https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html#cross-origin-opener-policy",
        "https://cheatsheetseries.owasp.org/cheatsheets/XS_Leaks_Cheat_Sheet.html#cross-origin-opener-policy-coop",
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy",
        "https://scotthelme.co.uk/coop-and-coep/",
    ],
    "Pragma": [
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Pragma",
    ],
    "Referrer-Policy": [
        "https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html#referrer-policy",
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy",
        "https://scotthelme.co.uk/a-new-security-header-referrer-policy/",
    ],
    "Server": [
        "https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html#server",
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Server",
    ],
    "Set-Cookie": [
        "https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html#set-cookie",
        "https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html#cookies",
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/set-cookie",
        "https://scotthelme.co.uk/tough-cookies/",
    ],
    "Strict-Transport-Security": [
        "https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Strict_Transport_Security_Cheat_Sheet.html",
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security",
        "https://scotthelme.co.uk/hsts-the-missing-link-in-tls/",
        "https://scotthelme.co.uk/hsts-cheat-sheet/",
    ],
    "User-Agent": [
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent",
    ],
    "X-AspNet-Version": [
        "https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html#x-aspnet-version",
    ],
    "X-Content-Type-Options": [
        "https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html#x-content-type-options",
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options",
    ],
    "X-Forwarded-For": [
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For",
    ],
    "X-Frame-Options": [
        "https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html#x-frame-options",
        "https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html#x-frame-options-header-types",  # noqa: E501 pylint: disable=line-too-long
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options",
    ],
    "X-Powered-By": [
        "https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html#x-powered-by",
    ],
    "X-XSS-Protection": [
        "https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html#x-xss-protection",
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection",
    ],
}


class DrHEADerParser(BaseParser, BaseFileParser):
    @classmethod
    def get_name(cls) -> str:
        return "DrHeader"

    @classmethod
    def get_filetype(cls) -> str:
        return Parser_Filetype.FILETYPE_JSON

    @classmethod
    def get_type(cls) -> str:
        return Parser_Type.TYPE_DAST

    def check_format(self, data: Any) -> bool:
        if (
            isinstance(data, list)  # pylint: disable=too-many-boolean-expressions
            and len(data) >= 1
            and isinstance(data[0], dict)
            and data[0].get("rule")
            and data[0].get("message")
            and data[0].get("severity")
        ):
            return True
        return False

    def get_observations(self, data: list, product: Product, branch: Optional[Branch]) -> list[Observation]:
        observations = []

        for drheader_observation in data:
            rule = drheader_observation.get("rule")
            message = drheader_observation.get("message")
            severity = drheader_observation.get("severity", Severity.SEVERITY_UNKNOWN)
            value = drheader_observation.get("value")
            expected = drheader_observation.get("expected")
            delimiter = drheader_observation.get("delimiter")

            if not rule:
                title = "No rule name"
            else:
                title = "Header: " + rule

            description = ""
            if message:
                description += message + "\n\n"
            if value:
                description += "**Value:** " + value + "\n\n"
            if expected:
                if isinstance(expected, list):
                    if len(expected) == 1:
                        description += "**Expected:** " + expected[0]
                    elif delimiter:
                        description += "**Expected:** "
                        description += (delimiter + " ").join(expected)
                    else:
                        description += "**Expected:**\n* "
                        description += "\n* ".join(expected)
                else:
                    description += "**Expected:** " + str(expected)

            observation = Observation(title=title, parser_severity=severity.title(), description=description)

            evidence = []
            evidence.append("Result")
            evidence.append(dumps(drheader_observation))
            observation.unsaved_evidences.append(evidence)

            references = REFERENCES.get(rule)
            if references:
                observation.unsaved_references = references

            observations.append(observation)
        return observations
