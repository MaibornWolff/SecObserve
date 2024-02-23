from constance import config
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
from application.vex.api.views import CSAFViewSet, OpenVEXViewSet

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
if config.FEATURE_VEX:
    router.register("vex/openvex", OpenVEXViewSet)
    router.register("vex/csaf", CSAFViewSet)

app_name = "api"
urlpatterns = router.urls
