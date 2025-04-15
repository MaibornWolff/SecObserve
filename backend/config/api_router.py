from rest_framework.routers import SimpleRouter

from application.access_control.api.views import (
    ApiTokenViewSet,
    AuthorizationGroupMemberViewSet,
    AuthorizationGroupViewSet,
    ProductApiTokenViewset,
    UserViewSet,
)
from application.core.api.views import (
    BranchNameViewSet,
    BranchViewSet,
    EvidenceViewSet,
    ObservationLogViewSet,
    ObservationTitleViewSet,
    ObservationViewSet,
    PotentialDuplicateViewSet,
    ProductAuthorizationGroupMemberViewSet,
    ProductGroupNameViewSet,
    ProductGroupViewSet,
    ProductMemberViewSet,
    ProductNameViewSet,
    ProductViewSet,
    ServiceViewSet,
)
from application.import_observations.api.views import (
    ApiConfigurationViewSet,
    ParserViewSet,
    VulnerabilityCheckViewSet,
)
from application.licenses.api.views import (
    LicenseComponentEvidenceViewSet,
    LicenseComponentIdViewSet,
    LicenseComponentViewSet,
    LicenseGroupAuthorizationGroupMemberViewSet,
    LicenseGroupMemberViewSet,
    LicenseGroupViewSet,
    LicensePolicyAuthorizationGroupMemberViewSet,
    LicensePolicyItemViewSet,
    LicensePolicyMemberViewSet,
    LicensePolicyViewSet,
    LicenseViewSet,
)
from application.notifications.api.views import NotificationViewSet
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
router.register("authorization_groups", AuthorizationGroupViewSet, basename="authorization_groups")
router.register(
    "authorization_group_members",
    AuthorizationGroupMemberViewSet,
    basename="authorization_group_members",
)
router.register("api_tokens", ApiTokenViewSet, basename="api_tokens")
router.register("product_api_tokens", ProductApiTokenViewset, basename="product_api_tokens")
router.register("products", ProductViewSet, basename="products")
router.register("product_names", ProductNameViewSet, basename="product_names")
router.register("product_groups", ProductGroupViewSet, basename="product_groups")
router.register("product_group_names", ProductGroupNameViewSet, basename="product_group_names")
router.register("product_members", ProductMemberViewSet, basename="product_members")
router.register(
    "product_authorization_group_members",
    ProductAuthorizationGroupMemberViewSet,
    basename="product_authorization_group_members",
)
router.register("branches", BranchViewSet, basename="branches")
router.register("branch_names", BranchNameViewSet, basename="branch_names")
router.register("services", ServiceViewSet, basename="services")
router.register("parsers", ParserViewSet, basename="parsers")
router.register("observations", ObservationViewSet, basename="observations")
router.register("observation_titles", ObservationTitleViewSet, basename="observation_titles")
router.register("observation_logs", ObservationLogViewSet, basename="observation_logs")
router.register("general_rules", GeneralRuleViewSet, basename="general_rules")
router.register("api_configurations", ApiConfigurationViewSet, basename="api_configurations")
router.register("product_rules", ProductRuleViewSet, basename="product_rules")
router.register("evidences", EvidenceViewSet, basename="evidences")
router.register("notifications", NotificationViewSet, basename="notifications")
router.register("vulnerability_checks", VulnerabilityCheckViewSet, basename="vulnerability_checks")
router.register("potential_duplicates", PotentialDuplicateViewSet, basename="potential_duplicates")
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
router.register("vex/openvex_branches", OpenVEXBranchViewSet, basename="openvex_branches")
router.register("vex/vex_counters", VEXCounterViewSet, basename="vex_counters")
router.register("vex/vex_documents", VEXDocumentViewSet, basename="vex_documents")
router.register("vex/vex_statements", VEXStatementViewSet, basename="vex_statements")

router.register("license_components", LicenseComponentViewSet, basename="license_components")
router.register("license_component_ids", LicenseComponentIdViewSet, basename="license_component_ids")
router.register(
    "license_component_evidences",
    LicenseComponentEvidenceViewSet,
    basename="license_component_evidences",
)
router.register("licenses", LicenseViewSet, basename="licenses")
router.register("license_groups", LicenseGroupViewSet, basename="license_groups")
router.register("license_group_members", LicenseGroupMemberViewSet, basename="license_group_members")
router.register(
    "license_group_authorization_group_members",
    LicenseGroupAuthorizationGroupMemberViewSet,
    basename="license_group_authorization_group_members",
)
router.register("license_policies", LicensePolicyViewSet, basename="license_policies")
router.register("license_policy_items", LicensePolicyItemViewSet, basename="license_policy_items")
router.register(
    "license_policy_members",
    LicensePolicyMemberViewSet,
    basename="license_policy_members",
)
router.register(
    "license_policy_authorization_group_members",
    LicensePolicyAuthorizationGroupMemberViewSet,
    basename="license_policy_authorization_group_members",
)

app_name = "api"
urlpatterns = router.urls
