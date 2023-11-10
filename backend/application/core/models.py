from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    CASCADE,
    PROTECT,
    SET_NULL,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    ForeignKey,
    Index,
    IntegerField,
    ManyToManyField,
    Model,
    TextField,
)
from django.utils import timezone

from application.access_control.models import User
from application.core.services.observation import (
    get_identity_hash,
    normalize_observation_fields,
)


class Product(Model):
    ISSUE_TRACKER_GITHUB = "GitHub"
    ISSUE_TRACKER_GITLAB = "GitLab"
    ISSUE_TRACKER_JIRA = "Jira"

    ISSUE_TRACKER_TYPE_CHOICES = [
        (ISSUE_TRACKER_GITHUB, ISSUE_TRACKER_GITHUB),
        (ISSUE_TRACKER_GITLAB, ISSUE_TRACKER_GITLAB),
        (ISSUE_TRACKER_JIRA, ISSUE_TRACKER_JIRA),
    ]

    name = CharField(max_length=255, unique=True)
    description = TextField(max_length=2048, blank=True)

    is_product_group = BooleanField(default=False)
    product_group = ForeignKey(
        "self", on_delete=PROTECT, related_name="products", null=True, blank=True
    )

    repository_prefix = CharField(max_length=255, blank=True)
    repository_default_branch = ForeignKey(
        "Branch",
        on_delete=SET_NULL,
        related_name="repository_default_branch",
        null=True,
    )
    repository_branch_housekeeping_active = BooleanField(null=True)
    repository_branch_housekeeping_keep_inactive_days = IntegerField(
        null=True, validators=[MinValueValidator(1), MaxValueValidator(999999)]
    )
    repository_branch_housekeeping_exempt_branches = CharField(
        max_length=255, blank=True
    )

    security_gate_passed = BooleanField(null=True)
    security_gate_active = BooleanField(null=True)
    security_gate_threshold_critical = IntegerField(
        null=True, validators=[MinValueValidator(0), MaxValueValidator(999999)]
    )
    security_gate_threshold_high = IntegerField(
        null=True, validators=[MinValueValidator(0), MaxValueValidator(999999)]
    )
    security_gate_threshold_medium = IntegerField(
        null=True, validators=[MinValueValidator(0), MaxValueValidator(999999)]
    )
    security_gate_threshold_low = IntegerField(
        null=True, validators=[MinValueValidator(0), MaxValueValidator(999999)]
    )
    security_gate_threshold_none = IntegerField(
        null=True, validators=[MinValueValidator(0), MaxValueValidator(999999)]
    )
    security_gate_threshold_unkown = IntegerField(
        null=True, validators=[MinValueValidator(0), MaxValueValidator(999999)]
    )

    members: ManyToManyField = ManyToManyField(
        User, through="Product_Member", related_name="product_members", blank=True
    )
    apply_general_rules = BooleanField(default=True)

    notification_ms_teams_webhook = CharField(max_length=255, blank=True)
    notification_email_to = CharField(max_length=255, blank=True)

    issue_tracker_active = BooleanField(default=False)
    issue_tracker_type = CharField(
        max_length=12, choices=ISSUE_TRACKER_TYPE_CHOICES, blank=True
    )
    issue_tracker_base_url = CharField(max_length=255, blank=True)
    issue_tracker_username = CharField(max_length=255, blank=True)
    issue_tracker_api_key = CharField(max_length=255, blank=True)
    issue_tracker_project_id = CharField(max_length=255, blank=True)
    issue_tracker_labels = CharField(max_length=255, blank=True)
    issue_tracker_issue_type = CharField(max_length=255, blank=True)
    issue_tracker_status_closed = CharField(max_length=255, blank=True)

    last_observation_change = DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name

    @property
    def open_critical_observation_count(self):
        if self.is_product_group:
            count = 0
            for product in Product.objects.filter(product_group=self):
                count += product.open_critical_observation_count
            return count

        return Observation.objects.filter(
            product=self,
            branch=self.repository_default_branch,
            current_status=Observation.STATUS_OPEN,
            current_severity=Observation.SEVERITY_CRITICAL,
        ).count()

    @property
    def open_high_observation_count(self):
        if self.is_product_group:
            count = 0
            for product in Product.objects.filter(product_group=self):
                count += product.open_high_observation_count
            return count

        return Observation.objects.filter(
            product=self,
            branch=self.repository_default_branch,
            current_status=Observation.STATUS_OPEN,
            current_severity=Observation.SEVERITY_HIGH,
        ).count()

    @property
    def open_medium_observation_count(self):
        if self.is_product_group:
            count = 0
            for product in Product.objects.filter(product_group=self):
                count += product.open_medium_observation_count
            return count

        return Observation.objects.filter(
            product=self,
            branch=self.repository_default_branch,
            current_status=Observation.STATUS_OPEN,
            current_severity=Observation.SEVERITY_MEDIUM,
        ).count()

    @property
    def open_low_observation_count(self):
        if self.is_product_group:
            count = 0
            for product in Product.objects.filter(product_group=self):
                count += product.open_low_observation_count
            return count

        return Observation.objects.filter(
            product=self,
            branch=self.repository_default_branch,
            current_status=Observation.STATUS_OPEN,
            current_severity=Observation.SEVERITY_LOW,
        ).count()

    @property
    def open_none_observation_count(self):
        if self.is_product_group:
            count = 0
            for product in Product.objects.filter(product_group=self):
                count += product.open_none_observation_count
            return count

        return Observation.objects.filter(
            product=self,
            branch=self.repository_default_branch,
            current_status=Observation.STATUS_OPEN,
            current_severity=Observation.SEVERITY_NONE,
        ).count()

    @property
    def open_unkown_observation_count(self):
        if self.is_product_group:
            count = 0
            for product in Product.objects.filter(product_group=self):
                count += product.open_unkown_observation_count
            return count

        return Observation.objects.filter(
            product=self,
            branch=self.repository_default_branch,
            current_status=Observation.STATUS_OPEN,
            current_severity=Observation.SEVERITY_UNKOWN,
        ).count()


class Branch(Model):
    product = ForeignKey(Product, on_delete=CASCADE)
    name = CharField(max_length=255)
    last_import = DateTimeField(null=True)
    housekeeping_protect = BooleanField(default=False)

    class Meta:
        unique_together = (
            "product",
            "name",
        )
        indexes = [
            Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name

    @property
    def open_critical_observation_count(self):
        return Observation.objects.filter(
            branch=self,
            current_severity=Observation.SEVERITY_CRITICAL,
            current_status=Observation.STATUS_OPEN,
        ).count()

    @property
    def open_high_observation_count(self):
        return Observation.objects.filter(
            branch=self,
            current_severity=Observation.SEVERITY_HIGH,
            current_status=Observation.STATUS_OPEN,
        ).count()

    @property
    def open_medium_observation_count(self):
        return Observation.objects.filter(
            branch=self,
            current_severity=Observation.SEVERITY_MEDIUM,
            current_status=Observation.STATUS_OPEN,
        ).count()

    @property
    def open_low_observation_count(self):
        return Observation.objects.filter(
            branch=self,
            current_severity=Observation.SEVERITY_LOW,
            current_status=Observation.STATUS_OPEN,
        ).count()

    @property
    def open_none_observation_count(self):
        return Observation.objects.filter(
            branch=self,
            current_severity=Observation.SEVERITY_NONE,
            current_status=Observation.STATUS_OPEN,
        ).count()

    @property
    def open_unkown_observation_count(self):
        return Observation.objects.filter(
            branch=self,
            current_severity=Observation.SEVERITY_UNKOWN,
            current_status=Observation.STATUS_OPEN,
        ).count()


class Service(Model):
    product = ForeignKey(Product, on_delete=CASCADE)
    name = CharField(max_length=255)

    class Meta:
        unique_together = (
            "product",
            "name",
        )
        indexes = [
            Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name

    @property
    def open_critical_observation_count(self):
        return Observation.objects.filter(
            origin_service=self,
            branch=self.product.repository_default_branch,
            current_severity=Observation.SEVERITY_CRITICAL,
            current_status=Observation.STATUS_OPEN,
        ).count()

    @property
    def open_high_observation_count(self):
        return Observation.objects.filter(
            origin_service=self,
            branch=self.product.repository_default_branch,
            current_severity=Observation.SEVERITY_HIGH,
            current_status=Observation.STATUS_OPEN,
        ).count()

    @property
    def open_medium_observation_count(self):
        return Observation.objects.filter(
            origin_service=self,
            branch=self.product.repository_default_branch,
            current_severity=Observation.SEVERITY_MEDIUM,
            current_status=Observation.STATUS_OPEN,
        ).count()

    @property
    def open_low_observation_count(self):
        return Observation.objects.filter(
            origin_service=self,
            branch=self.product.repository_default_branch,
            current_severity=Observation.SEVERITY_LOW,
            current_status=Observation.STATUS_OPEN,
        ).count()

    @property
    def open_none_observation_count(self):
        return Observation.objects.filter(
            origin_service=self,
            branch=self.product.repository_default_branch,
            current_severity=Observation.SEVERITY_NONE,
            current_status=Observation.STATUS_OPEN,
        ).count()

    @property
    def open_unkown_observation_count(self):
        return Observation.objects.filter(
            origin_service=self,
            branch=self.product.repository_default_branch,
            current_severity=Observation.SEVERITY_UNKOWN,
            current_status=Observation.STATUS_OPEN,
        ).count()


class Product_Member(Model):
    product = ForeignKey(Product, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)
    role = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = (
            "product",
            "user",
        )


class Parser(Model):
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

    SOURCE_API = "API"
    SOURCE_FILE = "File"
    SOURCE_MANUAL = "Manual"
    SOURCE_UNKOWN = "Unkown"

    SOURCE_CHOICES = [
        (SOURCE_API, SOURCE_API),
        (SOURCE_FILE, SOURCE_FILE),
        (SOURCE_MANUAL, SOURCE_MANUAL),
        (SOURCE_UNKOWN, SOURCE_UNKOWN),
    ]

    name = CharField(max_length=255, unique=True)
    type = CharField(max_length=16, choices=TYPE_CHOICES)
    source = CharField(max_length=16, choices=SOURCE_CHOICES)

    class Meta:
        indexes = [
            Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name


class Observation(Model):
    SEVERITY_UNKOWN = "Unkown"
    SEVERITY_NONE = "None"
    SEVERITY_LOW = "Low"
    SEVERITY_HIGH = "High"
    SEVERITY_MEDIUM = "Medium"
    SEVERITY_CRITICAL = "Critical"

    SEVERITY_CHOICES = [
        (SEVERITY_UNKOWN, SEVERITY_UNKOWN),
        (SEVERITY_NONE, SEVERITY_NONE),
        (SEVERITY_LOW, SEVERITY_LOW),
        (SEVERITY_MEDIUM, SEVERITY_MEDIUM),
        (SEVERITY_HIGH, SEVERITY_HIGH),
        (SEVERITY_CRITICAL, SEVERITY_CRITICAL),
    ]

    NUMERICAL_SEVERITIES = {
        SEVERITY_UNKOWN: 6,
        SEVERITY_NONE: 5,
        SEVERITY_LOW: 4,
        SEVERITY_MEDIUM: 3,
        SEVERITY_HIGH: 2,
        SEVERITY_CRITICAL: 1,
    }

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

    product = ForeignKey(Product, on_delete=PROTECT)
    branch = ForeignKey(Branch, on_delete=CASCADE, null=True)
    parser = ForeignKey(Parser, on_delete=PROTECT)
    title = CharField(max_length=255)
    description = TextField(max_length=2048, blank=True)
    recommendation = TextField(max_length=2048, blank=True)
    current_severity = CharField(max_length=12, choices=SEVERITY_CHOICES)
    numerical_severity = IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    parser_severity = CharField(max_length=12, choices=SEVERITY_CHOICES, blank=True)
    rule_severity = CharField(max_length=12, choices=SEVERITY_CHOICES, blank=True)
    assessment_severity = CharField(max_length=12, choices=SEVERITY_CHOICES, blank=True)
    current_status = CharField(max_length=16, choices=STATUS_CHOICES)
    parser_status = CharField(max_length=16, choices=STATUS_CHOICES, blank=True)
    rule_status = CharField(max_length=16, choices=STATUS_CHOICES, blank=True)
    assessment_status = CharField(max_length=16, choices=STATUS_CHOICES, blank=True)
    scanner_observation_id = CharField(max_length=255, blank=True)
    vulnerability_id = CharField(max_length=255, blank=True)
    origin_component_name = CharField(max_length=255, blank=True)
    origin_component_version = CharField(max_length=255, blank=True)
    origin_component_name_version = CharField(max_length=513, blank=True)
    origin_component_purl = CharField(max_length=255, blank=True)
    origin_component_cpe = CharField(max_length=255, blank=True)
    origin_docker_image_name = CharField(max_length=255, blank=True)
    origin_docker_image_tag = CharField(max_length=255, blank=True)
    origin_docker_image_name_tag = CharField(max_length=513, blank=True)
    origin_docker_image_name_tag_short = CharField(max_length=513, blank=True)
    origin_endpoint_url = TextField(max_length=2048, blank=True)
    origin_endpoint_scheme = CharField(max_length=255, blank=True)
    origin_endpoint_hostname = CharField(max_length=255, blank=True)
    origin_endpoint_port = IntegerField(
        null=True, validators=[MinValueValidator(0), MaxValueValidator(65535)]
    )
    origin_endpoint_path = TextField(max_length=2048, blank=True)
    origin_endpoint_params = TextField(max_length=2048, blank=True)
    origin_endpoint_query = TextField(max_length=2048, blank=True)
    origin_endpoint_fragment = TextField(max_length=2048, blank=True)
    origin_service_name = CharField(max_length=255, blank=True)
    origin_service = ForeignKey(Service, on_delete=PROTECT, null=True)
    origin_source_file = CharField(max_length=255, blank=True)
    origin_source_line_start = IntegerField(
        null=True, validators=[MinValueValidator(0), MaxValueValidator(999999)]
    )
    origin_source_line_end = IntegerField(
        null=True, validators=[MinValueValidator(0), MaxValueValidator(999999)]
    )
    cvss3_score = DecimalField(max_digits=3, decimal_places=1, null=True)
    cvss3_vector = CharField(max_length=255, blank=True)
    cwe = IntegerField(
        null=True, validators=[MinValueValidator(1), MaxValueValidator(999999)]
    )
    epss_score = DecimalField(
        max_digits=6,
        decimal_places=3,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    epss_percentile = DecimalField(
        max_digits=6,
        decimal_places=3,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    found = DateField(null=True)
    scanner = CharField(max_length=255, blank=True)
    upload_filename = CharField(max_length=255, blank=True)
    api_configuration_name = CharField(max_length=255, blank=True)
    import_last_seen = DateTimeField()
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)
    last_observation_log = DateTimeField(default=timezone.now)
    identity_hash = CharField(max_length=64)
    general_rule = ForeignKey(
        "rules.Rule",
        related_name="general_rules",
        blank=True,
        null=True,
        on_delete=PROTECT,
    )
    product_rule = ForeignKey(
        "rules.Rule",
        related_name="product_rules",
        blank=True,
        null=True,
        on_delete=PROTECT,
    )
    issue_tracker_issue_id = CharField(max_length=255, blank=True)
    issue_tracker_jira_initial_status = CharField(max_length=255, blank=True)

    class Meta:
        indexes = [
            Index(fields=["product", "branch"]),
            Index(fields=["title"]),
            Index(fields=["current_severity"]),
            Index(fields=["numerical_severity"]),
            Index(fields=["current_status"]),
            Index(fields=["vulnerability_id"]),
            Index(fields=["origin_component_name_version"]),
            Index(fields=["origin_docker_image_name_tag_short"]),
            Index(fields=["origin_service_name"]),
            Index(fields=["origin_endpoint_hostname"]),
            Index(fields=["origin_source_file"]),
            Index(fields=["last_observation_log"]),
            Index(fields=["epss_score"]),
            Index(fields=["scanner"]),
        ]

    def __str__(self):
        return f"{self.product} / {self.title}"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.unsaved_references = []
        self.unsaved_evidences = []

    def save(self, *args, **kwargs) -> None:
        normalize_observation_fields(self)
        self.identity_hash = get_identity_hash(self)

        return super().save(*args, **kwargs)


class Observation_Log(Model):
    observation = ForeignKey(
        Observation, related_name="observation_logs", on_delete=CASCADE
    )
    user = ForeignKey(
        "access_control.User", related_name="observation_logs", on_delete=PROTECT
    )
    severity = CharField(
        max_length=12, choices=Observation.SEVERITY_CHOICES, blank=True
    )
    status = CharField(max_length=16, choices=Observation.STATUS_CHOICES, blank=True)
    comment = CharField(max_length=255)
    created = DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            Index(fields=["observation", "-created"]),
            Index(fields=["-created"]),
        ]
        ordering = ["observation", "-created"]


class Evidence(Model):
    observation = ForeignKey(Observation, related_name="evidences", on_delete=CASCADE)
    name = CharField(max_length=255)
    evidence = TextField()

    class Meta:
        indexes = [
            Index(fields=["name"]),
        ]


class Reference(Model):
    observation = ForeignKey(Observation, related_name="references", on_delete=CASCADE)
    url = TextField(max_length=2048)
