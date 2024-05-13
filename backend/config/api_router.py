from rest_framework.routers import SimpleRouter

from application.access_control.api.views import (
    ApiTokenViewSet,
    AuthorizationGroupViewSet,
    ProductApiTokenViewset,
    UserViewSet,
)
from application.commons.api.views import NotificationViewSet
from application.core.api.views import (
    BranchViewSet,
    EvidenceViewSet,
    ObservationLogViewSet,
    ObservationViewSet,
    ParserViewSet,
    PotentialDuplicateViewSet,
    ProductAuthorizationGroupMemberViewSet,
    ProductGroupViewSet,
    ProductMemberViewSet,
    ProductViewSet,
    ServiceViewSet,
)
from application.import_observations.api.views import (
    ApiConfigurationViewSet,
    VulnerabilityCheckViewSet,
)
from application.rules.api.views import GeneralRuleViewSet, ProductRuleViewSet
from application.vex.api.views import (
    CSAFBranchViewSet,
    CSAFViewSet,
    CSAFVulnerabilityViewSet,
    OpenVEXBranchViewSet,
    OpenVEXViewSet,
    OpenVEXVulnerabilityViewSet,
    VEXCounterViewSet,
    VEXDocumentViewSet,
    VEXStatementViewSet,
)

router = SimpleRouter()

router.register("users", UserViewSet, basename="users")
router.register(
    "authorization_groups", AuthorizationGroupViewSet, basename="authorization_groups"
)
router.register("api_tokens", ApiTokenViewSet, basename="api_tokens")
router.register(
    "product_api_tokens", ProductApiTokenViewset, basename="product_api_tokens"
)
router.register("products", ProductViewSet, basename="products")
router.register("product_groups", ProductGroupViewSet, basename="product_groups")
router.register("product_members", ProductMemberViewSet, basename="product_members")
router.register(
    "product_authorization_group_members",
    ProductAuthorizationGroupMemberViewSet,
    basename="product_authorization_group_members",
)
router.register("branches", BranchViewSet, basename="branches")
router.register("services", ServiceViewSet, basename="services")
router.register("parsers", ParserViewSet, basename="parsers")
router.register("observations", ObservationViewSet, basename="observations")
router.register("observation_logs", ObservationLogViewSet, basename="observation_logs")
router.register("general_rules", GeneralRuleViewSet, basename="general_rules")
router.register(
    "api_configurations", ApiConfigurationViewSet, basename="api_configurations"
)
router.register("product_rules", ProductRuleViewSet, basename="product_rules")
router.register("evidences", EvidenceViewSet, basename="evidences")
router.register("notifications", NotificationViewSet, basename="notifications")
router.register(
    "vulnerability_checks", VulnerabilityCheckViewSet, basename="vulnerability_checks"
)
router.register(
    "potential_duplicates", PotentialDuplicateViewSet, basename="potential_duplicates"
)
router.register("vex/csaf", CSAFViewSet, basename="csaf")
router.register(
    "vex/csaf_vulnerabilities",
    CSAFVulnerabilityViewSet,
    basename="csaf_vulnerabilities",
)
router.register("vex/csaf_branches", CSAFBranchViewSet, basename="csaf_branches")
router.register("vex/openvex", OpenVEXViewSet, basename="openvex")
router.register(
    "vex/openvex_vulnerabilities",
    OpenVEXVulnerabilityViewSet,
    basename="openvex_vulnerabilities",
)
router.register(
    "vex/openvex_branches", OpenVEXBranchViewSet, basename="openvex_branches"
)
router.register("vex/vex_counters", VEXCounterViewSet, basename="vex_counters")
router.register("vex/vex_documents", VEXDocumentViewSet, basename="vex_documents")
router.register("vex/vex_statements", VEXStatementViewSet, basename="vex_statements")

app_name = "api"
urlpatterns = router.urls
