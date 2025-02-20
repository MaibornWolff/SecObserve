from typing import Any, Optional

from semver import Version


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


class ExtendedSemVer:
    def __init__(self) -> None:
        self.prefix: Optional[int] = None
        self.semver: Version

    @classmethod
    def parse(cls, version: Optional[str]) -> Optional["ExtendedSemVer"]:
        if not version:
            return None

        instance = cls()

        elements = version.split(":")
        if len(elements) >= 2:
            prefix = elements[0]
            if not prefix.isdigit():
                return None
            instance.prefix = int(prefix)

            suffix = ":".join(elements[1:])
        else:
            suffix = version

        suffix_semver = instance._get_semver(suffix)
        if not suffix_semver:
            return None
        instance.semver = suffix_semver

        return instance

    @classmethod
    def _get_semver(cls, suffix: str) -> Optional[Version]:
        if not suffix:
            return None

        # Go packages sometimes have a "v" prefix
        if suffix.startswith("v"):
            suffix = suffix[1:]

        if suffix == "0":
            return Version.parse("0.0.0")

        if len(suffix.split("-")) == 2:
            prefix = suffix.split("-")[0]
            if len(prefix.split(".")) == 2:
                prefix = f"{prefix}.0"
            suffix = f"{prefix}-{suffix.split('-')[1]}"

        if len(suffix.split(".")) == 2:
            suffix = f"{suffix}.0"

        if not Version.is_valid(suffix):
            return None

        return Version.parse(suffix)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False

        if (self.prefix is None and other.prefix is not None) or (self.prefix is not None and other.prefix is None):
            return False

        if self.prefix is not None and other.prefix is not None:
            if self.prefix < other.prefix:
                return False
            if self.prefix > other.prefix:
                return True

        return self.semver > other.semver

    def __ge__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False

        if (self.prefix is None and other.prefix is not None) or (self.prefix is not None and other.prefix is None):
            return False

        if self.prefix is not None and other.prefix is not None:
            if self.prefix < other.prefix:
                return False
            if self.prefix > other.prefix:
                return True

        return self.semver >= other.semver

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False

        if (self.prefix is None and other.prefix is not None) or (self.prefix is not None and other.prefix is None):
            return False

        if self.prefix is not None and other.prefix is not None:
            if self.prefix > other.prefix:
                return False
            if self.prefix < other.prefix:
                return True

        return self.semver < other.semver

    def __le__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False

        if (self.prefix is None and other.prefix is not None) or (self.prefix is not None and other.prefix is None):
            return False

        if self.prefix is not None and other.prefix is not None:
            if self.prefix > other.prefix:
                return False
            if self.prefix < other.prefix:
                return True

        return self.semver <= other.semver
