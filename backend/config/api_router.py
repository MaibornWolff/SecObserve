from rest_framework.routers import SimpleRouter

from application.access_control.api.views import UserViewSet
from application.core.api.views import (
    ObservationViewSet,
    ProductViewSet,
    ProductMemberViewSet,
    ParserViewSet,
    EvidenceViewSet,
)
from application.import_observations.api.views import ApiConfigurationViewSet
from application.rules.api.views import GeneralRuleViewSet, ProductRuleViewSet

router = SimpleRouter()

router.register("users", UserViewSet)
router.register("products", ProductViewSet)
router.register("product_members", ProductMemberViewSet)
router.register("parsers", ParserViewSet)
router.register("observations", ObservationViewSet)
router.register("general_rules", GeneralRuleViewSet)
router.register("api_configurations", ApiConfigurationViewSet)
router.register("product_rules", ProductRuleViewSet)
router.register("evidences", EvidenceViewSet)

app_name = "api"
urlpatterns = router.urls
