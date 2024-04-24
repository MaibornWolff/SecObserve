from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    IntegerField,
    Model,
    TextField,
)

from application.access_control.models import User
from application.core.models import Observation, Product


class Notification(Model):
    TYPE_EXCEPTION = "Exception"
    TYPE_SECURITY_GATE = "Security gate"
    TYPE_TASK = "Task"

    TYPE_CHOICES = [
        (TYPE_EXCEPTION, TYPE_EXCEPTION),
        (TYPE_SECURITY_GATE, TYPE_SECURITY_GATE),
        (TYPE_TASK, TYPE_TASK),
    ]

    name = CharField(max_length=255)
    created = DateTimeField(auto_now_add=True)
    message = TextField(max_length=4096)
    user = ForeignKey(User, on_delete=CASCADE, null=True)
    product = ForeignKey(Product, on_delete=CASCADE, null=True)
    observation = ForeignKey(Observation, on_delete=CASCADE, null=True)
    type = CharField(max_length=20, choices=TYPE_CHOICES)
    function = CharField(max_length=255, blank=True)
    arguments = TextField(max_length=4096, blank=True)


class Settings(Model):
    security_gate_active = BooleanField(
        default=True, help_text="Is the security gate activated?"
    )
    security_gate_threshold_critical = IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(999999)],
        help_text="Number of critical observations that must not be exceeded",
    )
    security_gate_threshold_high = IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(999999)],
        help_text="Number of high observations that must not be exceeded",
    )
    security_gate_threshold_medium = IntegerField(
        default=99999,
        validators=[MinValueValidator(0), MaxValueValidator(999999)],
        help_text="Number of medium observations that must not be exceeded",
    )
    security_gate_threshold_low = IntegerField(
        default=99999,
        validators=[MinValueValidator(0), MaxValueValidator(999999)],
        help_text="Number of low observations that must not be exceeded",
    )
    security_gate_threshold_none = IntegerField(
        default=99999,
        validators=[MinValueValidator(0), MaxValueValidator(999999)],
        help_text="Number of none observations that must not be exceeded",
    )
    security_gate_threshold_unkown = IntegerField(
        default=99999,
        validators=[MinValueValidator(0), MaxValueValidator(999999)],
        help_text="Number of unkown observations that must not be exceeded",
    )

    jwt_validity_duration_user = IntegerField(
        default=168,
        validators=[MinValueValidator(0), MaxValueValidator(999999)],
        help_text="Validity duration of JWT tokens for regular users in hours",
    )
    jwt_validity_duration_superuser = IntegerField(
        default=24,
        validators=[MinValueValidator(0), MaxValueValidator(999999)],
        help_text="Validity duration of JWT tokens for superusers in hours",
    )

    base_url_frontend = CharField(
        max_length=255,
        default="",
        help_text="Base URL of the frontend, used to set links in notifications correctly",
    )

    exception_ms_teams_webhook = CharField(
        max_length=255,
        blank=True,
        help_text="MS Teams webhook to send exception notifications",
    )
    exception_slack_webhook = CharField(
        max_length=255,
        blank=True,
        help_text="Slack webhook to send exception notifications",
    )
    exception_rate_limit = IntegerField(
        default=3600,
        validators=[MinValueValidator(0), MaxValueValidator(999999)],
        help_text="Timedelta in seconds when to send the same exception the next time",
    )
    email_from = CharField(
        max_length=255,
        blank=True,
        help_text="From address for sending email notifications",
    )
    exception_email_to = CharField(
        max_length=255,
        blank=True,
        help_text="Comma separated email addresses to send exception notifications",
    )

    background_product_metrics_interval_minutes = IntegerField(
        default=5,
        validators=[MinValueValidator(0), MaxValueValidator(999999)],
        help_text="Calculate product metrics every x minutes",
    )
    background_epss_import_crontab_minutes = IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(59)],
        help_text="Minutes crontab expression for EPSS import",
    )
    background_epss_import_crontab_hours = IntegerField(
        default=3,
        validators=[MinValueValidator(0), MaxValueValidator(23)],
        help_text="Hours crontab expression for EPSS import (UTC)",
    )

    branch_housekeeping_crontab_minutes = IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(59)],
        help_text="Minutes crontab expression for branch housekeeping",
    )
    branch_housekeeping_crontab_hours = IntegerField(
        default=2,
        validators=[MinValueValidator(0), MaxValueValidator(23)],
        help_text="Hours crontab expression for branch housekeeping (UTC)",
    )
    branch_housekeeping_active = BooleanField(
        default=True, help_text="Delete inactive branches"
    )
    branch_housekeeping_keep_inactive_days = IntegerField(
        default=30,
        validators=[MinValueValidator(0), MaxValueValidator(999999)],
        help_text="Days before incative branches and their observations are deleted",
    )
    branch_housekeeping_exempt_branches = CharField(
        max_length=255,
        blank=True,
        help_text="Regular expression which branches to exempt from deletion",
    )

    feature_vex = BooleanField(
        default=False, help_text="Generate VEX documents in OpenVEX and CSAF format"
    )

    def save(self, *args, **kwargs):
        """
        Save object to the database. Removes all other entries if there
        are any.
        """
        self.__class__.objects.exclude(id=self.pk).delete()
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """
        Load object from the database. Failing that, create a new empty
        (default) instance of the object and return it (without saving it
        to the database).
        """
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()
