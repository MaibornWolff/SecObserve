from django.test import TestCase

from application.access_control.models import (
    Authorization_Group,
    Authorization_Group_Member,
    User,
)
from application.authorization.services.roles_permissions import Roles
from application.core.models import (
    Branch,
    Observation,
    Observation_Log,
    Product,
    Product_Authorization_Group_Member,
    Product_Member,
    Service,
)
from application.core.types import Severity, Status
from application.import_observations.models import (
    Api_Configuration,
    Parser,
    Vulnerability_Check,
)
from application.rules.models import Rule
from application.vex.models import OpenVEX


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None

        self.user_internal = User(id=1, username="user_internal@example.com", is_external=False)
        self.user_external = User(username="user_external@example.com", is_external=True)
        self.user_admin = User(id=2, username="user_admin@example.com", is_superuser=True)

        self.parser_1 = Parser(name="parser_1")
        self.product_group_1 = Product(name="product_group_1")
        self.product_1 = Product(name="product_1")
        self.observation_1 = Observation(title="observation_1", product=self.product_1)
        self.observation_log_1 = Observation_Log(
            observation=self.observation_1,
            user=self.user_internal,
            severity=Severity.SEVERITY_CRITICAL,
            status=Status.STATUS_DUPLICATE,
            comment="comment",
        )
        self.product_rule_1 = Rule(name="rule_1", product=self.product_1)
        self.api_configuration_1 = Api_Configuration(
            name="api_configuration_1", product=self.product_1, parser=self.parser_1
        )

        self.branch_1 = Branch(name="branch_1", product=self.product_1)
        self.product_1.repository_default_branch = self.branch_1
        self.observation_1.branch = self.branch_1
        self.branch_2 = Branch(name="branch_2", product=self.product_1)

        self.service_1 = Service(name="service_1", product=self.product_1)

        self.product_member_1 = Product_Member(product=self.product_1, user=self.user_internal, role=Roles.Writer)

        self.authorization_group_1 = Authorization_Group(name="authorization_group_1")
        self.authorization_group_member_1 = Authorization_Group_Member(
            authorization_group=self.authorization_group_1,
            user=self.user_internal,
            is_manager=True,
        )
        self.product_authorization_group_member_1 = Product_Authorization_Group_Member(
            product=self.product_1,
            authorization_group=self.authorization_group_1,
            role=Roles.Writer,
        )

        self.openvex_1 = OpenVEX(
            user=self.user_external,
            product=self.product_1,
        )

        self.vulnerability_check_1 = Vulnerability_Check(product=self.product_1)
        self.general_rule = Rule(name="general_rule")
