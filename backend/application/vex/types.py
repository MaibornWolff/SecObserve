from dataclasses import dataclass
from typing import Optional


class CSAF_Tracking_Status:
    CSAF_TRACKING_STATUS_DRAFT = "draft"
    CSAF_TRACKING_STATUS_FINAL = "final"
    CSAF_TRACKING_STATUS_INTERIM = "interim"

    CSAF_TRACKING_STATUS_CHOICES = [
        (CSAF_TRACKING_STATUS_DRAFT, CSAF_TRACKING_STATUS_DRAFT),
        (CSAF_TRACKING_STATUS_FINAL, CSAF_TRACKING_STATUS_FINAL),
        (CSAF_TRACKING_STATUS_INTERIM, CSAF_TRACKING_STATUS_INTERIM),
    ]


class CSAF_Publisher_Category:
    CSAF_PUBLISHER_CATEGORY_COORDINATOR = "coordinator"
    CSAF_PUBLISHER_CATEGORY_DISCOVERER = "discoverer"
    CSAF_PUBLISHER_CATEGORY_OTHER = "other"
    CSAF_PUBLISHER_CATEGORY_TRANSLATOR = "translator"
    CSAF_PUBLISHER_CATEGORY_USER = "user"
    CSAF_PUBLISHER_CATEGORY_VENDOR = "vendor"

    CSAF_PUBLISHER_CATEGORY_CHOICES = [
        (CSAF_PUBLISHER_CATEGORY_COORDINATOR, CSAF_PUBLISHER_CATEGORY_COORDINATOR),
        (CSAF_PUBLISHER_CATEGORY_DISCOVERER, CSAF_PUBLISHER_CATEGORY_DISCOVERER),
        (CSAF_PUBLISHER_CATEGORY_OTHER, CSAF_PUBLISHER_CATEGORY_OTHER),
        (CSAF_PUBLISHER_CATEGORY_TRANSLATOR, CSAF_PUBLISHER_CATEGORY_TRANSLATOR),
        (CSAF_PUBLISHER_CATEGORY_USER, CSAF_PUBLISHER_CATEGORY_USER),
        (CSAF_PUBLISHER_CATEGORY_VENDOR, CSAF_PUBLISHER_CATEGORY_VENDOR),
    ]


@dataclass(frozen=True)
class CSAFFullProductName:
    name: str
    product_id: str
    # product_identification_helper is still missing


@dataclass()
class CSAFProductTree:
    full_product_names: list[CSAFFullProductName]


@dataclass(frozen=True)
class CSAFNote:
    category: str
    text: str


@dataclass(frozen=True)
class CSAFFlag:
    label: str
    product_ids: list[str]


@dataclass(frozen=True)
class CSAFId:
    system_name: str
    text: str


@dataclass()
class CSAFProductStatus:
    fixed: list[str]
    known_affected: list[str]
    known_not_affected: list[str]
    under_investigation: list[str]


@dataclass()
class CSAFVulnerability:
    cve: str
    notes: list[CSAFNote]
    flags: list[CSAFFlag]
    ids: list[CSAFId]
    product_status: CSAFProductStatus
    # remediations are still missing


@dataclass()
class CSAFPublisher:
    name: str
    category: str
    namespace: str


@dataclass()
class CSAFEngine:
    name: str
    version: str


@dataclass()
class CSAFGenerator:
    engine: str


@dataclass(frozen=True)
class CSAFRevisionHistory:
    date: str
    number: str
    summary: str


@dataclass()
class CSAFTracking:
    id: str
    initial_release_date: str
    current_release_date: str
    version: str
    status: str
    generator: CSAFGenerator
    revision_history: list[CSAFRevisionHistory]


@dataclass()
class CSAFDocument:
    category: str
    csaf_version: str
    title: str
    publisher: CSAFPublisher
    tracking: CSAFTracking


@dataclass()
class CSAFRoot:
    document: CSAFDocument
    product_tree: CSAFProductTree
    vulnerabilities: list[CSAFVulnerability]

    def get_base_id(self) -> str:
        if len(self.document.tracking.id) > 36:
            return self.document.tracking.id[-36:]
        return ""


class OpenVEX_Status:
    OPEN_VEX_STATUS_NOT_AFFECTED = "not_affected"
    OPEN_VEX_STATUS_AFFECTED = "affected"
    OPEN_VEX_STATUS_FIXED = "fixed"
    OPEN_VEX_STATUS_UNDER_INVESTIGATION = "under_investigation"


@dataclass(frozen=True)
class OpenVEXProduct:
    id: str


@dataclass()
class OpenVEXVulnerability:
    id: Optional[str]
    name: str
    description: Optional[str] = None


@dataclass
class OpenVEXStatement:
    status: str
    status_notes: Optional[str]
    justification: Optional[str]
    action_statement: Optional[str]
    vulnerability: Optional[OpenVEXVulnerability]
    products: list[OpenVEXProduct]


@dataclass
class OpenVEXDocument:
    context: str
    id: str
    version: int
    author: str
    role: str
    timestamp: str
    last_updated: str
    tooling: str
    statements: list[OpenVEXStatement]

    def get_base_id(self) -> str:
        if len(self.id) > 36:
            return self.id[-36:]
        return ""
