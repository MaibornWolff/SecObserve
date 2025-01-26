class Severity:
    SEVERITY_UNKNOWN = "Unknown"
    SEVERITY_NONE = "None"
    SEVERITY_LOW = "Low"
    SEVERITY_HIGH = "High"
    SEVERITY_MEDIUM = "Medium"
    SEVERITY_CRITICAL = "Critical"

    SEVERITY_CHOICES = [
        (SEVERITY_UNKNOWN, SEVERITY_UNKNOWN),
        (SEVERITY_NONE, SEVERITY_NONE),
        (SEVERITY_LOW, SEVERITY_LOW),
        (SEVERITY_MEDIUM, SEVERITY_MEDIUM),
        (SEVERITY_HIGH, SEVERITY_HIGH),
        (SEVERITY_CRITICAL, SEVERITY_CRITICAL),
    ]

    NUMERICAL_SEVERITIES = {
        SEVERITY_UNKNOWN: 6,
        SEVERITY_NONE: 5,
        SEVERITY_LOW: 4,
        SEVERITY_MEDIUM: 3,
        SEVERITY_HIGH: 2,
        SEVERITY_CRITICAL: 1,
    }


class Status:
    STATUS_OPEN = "Open"
    STATUS_RESOLVED = "Resolved"
    STATUS_DUPLICATE = "Duplicate"
    STATUS_FALSE_POSITIVE = "False positive"
    STATUS_IN_REVIEW = "In review"
    STATUS_NOT_AFFECTED = "Not affected"
    STATUS_NOT_SECURITY = "Not security"
    STATUS_RISK_ACCEPTED = "Risk accepted"

    STATUS_CHOICES = [
        (STATUS_OPEN, STATUS_OPEN),
        (STATUS_RESOLVED, STATUS_RESOLVED),
        (STATUS_DUPLICATE, STATUS_DUPLICATE),
        (STATUS_FALSE_POSITIVE, STATUS_FALSE_POSITIVE),
        (STATUS_IN_REVIEW, STATUS_IN_REVIEW),
        (STATUS_NOT_AFFECTED, STATUS_NOT_AFFECTED),
        (STATUS_NOT_SECURITY, STATUS_NOT_SECURITY),
        (STATUS_RISK_ACCEPTED, STATUS_RISK_ACCEPTED),
    ]


class Assessment_Status:
    ASSESSMENT_STATUS_APPROVED = "Approved"
    ASSESSMENT_STATUS_NEEDS_APPROVAL = "Needs approval"
    ASSESSMENT_STATUS_REJECTED = "Rejected"
    ASSESSMENT_STATUS_AUTO_APPROVED = "Auto approved"
    ASSESSMENT_STATUS_REMOVED = "Removed"

    ASSESSMENT_STATUS_CHOICES = [
        (ASSESSMENT_STATUS_APPROVED, ASSESSMENT_STATUS_APPROVED),
        (ASSESSMENT_STATUS_NEEDS_APPROVAL, ASSESSMENT_STATUS_NEEDS_APPROVAL),
        (ASSESSMENT_STATUS_REJECTED, ASSESSMENT_STATUS_REJECTED),
        (ASSESSMENT_STATUS_AUTO_APPROVED, ASSESSMENT_STATUS_AUTO_APPROVED),
        (ASSESSMENT_STATUS_REMOVED, ASSESSMENT_STATUS_REMOVED),
    ]

    ASSESSMENT_STATUS_CHOICES_APPROVAL = [
        (ASSESSMENT_STATUS_APPROVED, ASSESSMENT_STATUS_APPROVED),
        (ASSESSMENT_STATUS_REJECTED, ASSESSMENT_STATUS_REJECTED),
    ]


class VexJustification:
    STATUS_COMPONENT_NOT_PRESENT = "component_not_present"
    STATUS_VULNERABLE_CODE_NOT_PRESENT = "vulnerable_code_not_present"
    STATUS_VULNERABLE_CODE_CANNOT_BE_CONTROLLED_BY_ADVERSARY = (
        "vulnerable_code_cannot_be_controlled_by_adversary"
    )
    STATUS_VULNERABLE_CODE_NOT_IN_EXECUTE_PATH = "vulnerable_code_not_in_execute_path"
    STATUS_INLINE_MITIGATIONS_ALREADY_EXIST = "inline_mitigations_already_exist"

    VEX_JUSTIFICATION_CHOICES = [
        (STATUS_COMPONENT_NOT_PRESENT, "Component not present"),
        (STATUS_VULNERABLE_CODE_NOT_PRESENT, "Vulnerable code not present"),
        (
            STATUS_VULNERABLE_CODE_CANNOT_BE_CONTROLLED_BY_ADVERSARY,
            "Vulnerable code cannot be controlled by adversary",
        ),
        (
            STATUS_VULNERABLE_CODE_NOT_IN_EXECUTE_PATH,
            "Vulnerable code not in execute path",
        ),
        (STATUS_INLINE_MITIGATIONS_ALREADY_EXIST, "Inline mitigations already exist"),
    ]


class PURL_Type:
    PURL_TYPE_CHOICES = {
        "alpm": "alpm",
        "apk": "APK",
        "bitbucket": "Bitbucket",
        "bitnami": "Bitnami",
        "cargo": "Rust",
        "cocoapods": "Cocoapods",
        "composer": "Composer",
        "conan": "Conan",
        "conda": "Conda",
        "cpan": "CPAN Perl",
        "cran": "CRAN R",
        "deb": "Debian",
        "docker": "Docker",
        "gem": "Ruby Gem",
        "generic": "Generic",
        "github": "GitHub",
        "golang": "Go",
        "hackage": "Hackage",
        "hex": "Hex",
        "huggingface": "Huggingface",
        "luarocks": "Lua",
        "maven": "Maven",
        "mlflow": "MLflow",
        "npm": "NPM",
        "nuget": "NuGet",
        "oci": "OCI",
        "pub": "Dart",
        "pypi": "PyPI",
        "rpm": "RPM",
        "qpkg": "QNX",
        "swid": "SWID",
        "swift": "Swift",
    }


class OSVLinuxEcosystem:
    ECOSYSTEM_ALMALINUX = "AlmaLinux"
    ECOSYSTEM_ALPINE = "Alpine"
    ECOSYSTEM_DEBIAN = "Debian"
    ECOSYSTEM_MAGEIA = "Mageia"
    ECOSYSTEM_OPENSUSE = "openSUSE"
    ECOSYSTEM_PHOTON_OS = "Photon OS"
    ECOSYSTEM_REDHAT = "Red Hat"
    ECOSYSTEM_ROCKY_LINUX = "Rocky Linux"
    ECOSYSTEM_SUSE = "SUSE"
    ECOSYSTEM_UBUNTU = "Ubuntu"

    OSV_LINUX_ECOSYSTEM_CHOICES = [
        (ECOSYSTEM_ALMALINUX, ECOSYSTEM_ALMALINUX),
        (ECOSYSTEM_ALPINE, ECOSYSTEM_ALPINE),
        (ECOSYSTEM_DEBIAN, ECOSYSTEM_DEBIAN),
        (ECOSYSTEM_MAGEIA, ECOSYSTEM_MAGEIA),
        (ECOSYSTEM_OPENSUSE, ECOSYSTEM_OPENSUSE),
        (ECOSYSTEM_PHOTON_OS, ECOSYSTEM_PHOTON_OS),
        (ECOSYSTEM_REDHAT, ECOSYSTEM_REDHAT),
        (ECOSYSTEM_ROCKY_LINUX, ECOSYSTEM_ROCKY_LINUX),
        (ECOSYSTEM_SUSE, ECOSYSTEM_SUSE),
        (ECOSYSTEM_UBUNTU, ECOSYSTEM_UBUNTU),
    ]
