from rest_framework.routers import SimpleRouter

from application.access_control.api.views import ProductApiTokenViewset, UserViewSet
from application.commons.api.views import NotificationViewSet
from application.core.api.views import (
    BranchViewSet,
    EvidenceViewSet,
    ObservationViewSet,
    ParserViewSet,
    ProductMemberViewSet,
    ProductViewSet,
)
from application.import_observations.api.views import ApiConfigurationViewSet
from application.metrics.api.views import ProductMetricsViewSet
from application.rules.api.views import GeneralRuleViewSet, ProductRuleViewSet

router = SimpleRouter()

router.register("users", UserViewSet)
router.register(
    "product_api_tokens", ProductApiTokenViewset, basename="product_api_tokens"
)
router.register("products", ProductViewSet)
router.register("product_members", ProductMemberViewSet)
router.register("branches", BranchViewSet)
router.register("parsers", ParserViewSet)
router.register("observations", ObservationViewSet)
router.register("general_rules", GeneralRuleViewSet)
router.register("api_configurations", ApiConfigurationViewSet)
router.register("product_rules", ProductRuleViewSet)
router.register("evidences", EvidenceViewSet)
router.register("notifications", NotificationViewSet)
router.register("metrics/product_metrics", ProductMetricsViewSet)

app_name = "api"
urlpatterns = router.urls
