from rest_framework.routers import SimpleRouter

from application.access_control.api.views import ProductApiTokenViewset, UserViewSet
from application.commons.api.views import NotificationViewSet
from application.core.api.views import (
    BranchViewSet,
    EvidenceViewSet,
    ObservationViewSet,
    ParserViewSet,
    PotentialDuplicateViewSet,
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
)

router = SimpleRouter()

router.register("users", UserViewSet)
router.register(
    "product_api_tokens", ProductApiTokenViewset, basename="product_api_tokens"
)
router.register("products", ProductViewSet)
router.register("product_groups", ProductGroupViewSet)
router.register("product_members", ProductMemberViewSet)
router.register("branches", BranchViewSet)
router.register("services", ServiceViewSet)
router.register("parsers", ParserViewSet)
router.register("observations", ObservationViewSet)
router.register("general_rules", GeneralRuleViewSet)
router.register("api_configurations", ApiConfigurationViewSet)
router.register("product_rules", ProductRuleViewSet)
router.register("evidences", EvidenceViewSet)
router.register("notifications", NotificationViewSet)
router.register("vulnerability_checks", VulnerabilityCheckViewSet)
router.register("potential_duplicates", PotentialDuplicateViewSet)
router.register("vex/csaf", CSAFViewSet)
router.register("vex/csaf_vulnerabilities", CSAFVulnerabilityViewSet)
router.register("vex/csaf_branches", CSAFBranchViewSet)
router.register("vex/openvex", OpenVEXViewSet)
router.register("vex/openvex_vulnerabilities", OpenVEXVulnerabilityViewSet)
router.register("vex/openvex_branches", OpenVEXBranchViewSet)

app_name = "api"
urlpatterns = router.urls
