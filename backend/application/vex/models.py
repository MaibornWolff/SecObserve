from typing import Any

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    Index,
    IntegerField,
    Model,
    TextField,
)
from django.utils import timezone

from application.access_control.models import User
from application.core.models import Branch, Product
from application.vex.types import (
    CSAF_Publisher_Category,
    CSAF_TLP_Label,
    CSAF_Tracking_Status,
    VEX_Document_Type,
    VEX_Justification,
    VEX_Status,
)


class VEX_Counter(Model):
    document_id_prefix = CharField(max_length=255)
    year = IntegerField(validators=[MinValueValidator(2000), MaxValueValidator(9999)])
    counter = IntegerField(default=0)

    class Meta:
        verbose_name = "VEX Counter"
        verbose_name_plural = "VEX Counters"
        unique_together = (
            "document_id_prefix",
            "year",
        )


class VEX_Base(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=CASCADE, null=True)
    document_id_prefix = CharField(max_length=255)
    document_base_id = CharField(max_length=36)
    version = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)])
    content_hash = CharField(max_length=256, blank=True)

    class Meta:
        abstract = True
        unique_together = (
            "document_id_prefix",
            "document_base_id",
        )


class OpenVEX(VEX_Base):
    id_namespace = CharField(max_length=255)
    author = CharField(max_length=255)
    role = CharField(max_length=255, blank=True)
    timestamp = DateTimeField()
    last_updated = DateTimeField()

    # Make sure that timestamp and last updated date are exactly the
    # same when creating a new CSAF record
    def save(self, *args: Any, **kwargs: Any) -> None:
        now = timezone.now()
        if not self.timestamp:
            self.timestamp = now
        self.last_updated = now
        super().save(*args, **kwargs)


class OpenVEX_Branch(Model):
    openvex = ForeignKey(OpenVEX, related_name="branches", on_delete=CASCADE)
    branch = ForeignKey(Branch, related_name="openvexes", on_delete=CASCADE)


class OpenVEX_Vulnerability(Model):
    openvex = ForeignKey(OpenVEX, related_name="vulnerability_names", on_delete=CASCADE)
    name = CharField(max_length=255)


class CSAF(VEX_Base):
    title = CharField(max_length=255)
    tlp_label = CharField(max_length=16, choices=CSAF_TLP_Label.CSAF_TLP_LABEL_CHOICES)
    tracking_initial_release_date = DateTimeField()
    tracking_current_release_date = DateTimeField()
    tracking_status = CharField(max_length=16, choices=CSAF_Tracking_Status.CSAF_TRACKING_STATUS_CHOICES)
    publisher_name = CharField(max_length=255)
    publisher_category = CharField(max_length=16, choices=CSAF_Publisher_Category.CSAF_PUBLISHER_CATEGORY_CHOICES)
    publisher_namespace = CharField(max_length=255)

    # Make sure that initial release date and current release date are exactly the
    # same when creating a new CSAF record
    def save(self, *args: Any, **kwargs: Any) -> None:
        now = timezone.now()
        if not self.tracking_initial_release_date:
            self.tracking_initial_release_date = now
        self.tracking_current_release_date = now
        super().save(*args, **kwargs)


class CSAF_Vulnerability(Model):
    csaf = ForeignKey(CSAF, related_name="vulnerability_names", on_delete=CASCADE)
    name = CharField(max_length=255)


class CSAF_Branch(Model):
    csaf = ForeignKey(CSAF, related_name="branches", on_delete=CASCADE)
    branch = ForeignKey(Branch, related_name="csafs", on_delete=CASCADE)


class CSAF_Revision(Model):
    csaf = ForeignKey(CSAF, related_name="revisions", on_delete=CASCADE)
    date = DateTimeField()
    version = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)])
    summary = TextField(max_length=255)


class CycloneDX(VEX_Base):
    author = CharField(max_length=255, blank=True)
    manufacturer = CharField(max_length=255, blank=True)
    first_issued = DateTimeField()
    last_updated = DateTimeField()


class CycloneDX_Branch(Model):
    cyclonedx = ForeignKey(CycloneDX, related_name="branches", on_delete=CASCADE)
    branch = ForeignKey(Branch, related_name="cyclonedxes", on_delete=CASCADE)


class CycloneDX_Vulnerability(Model):
    cyclonedx = ForeignKey(CycloneDX, related_name="vulnerability_names", on_delete=CASCADE)
    name = CharField(max_length=255)


class VEX_Document(Model):
    type = CharField(max_length=16, choices=VEX_Document_Type.VEX_DOCUMENT_TYPE_CHOICES)
    document_id = CharField(max_length=255)
    version = CharField(max_length=255)
    current_release_date = DateTimeField()
    initial_release_date = DateTimeField()
    author = CharField(max_length=255)
    role = CharField(max_length=255, blank=True)

    class Meta:
        unique_together = (
            "document_id",
            "author",
        )


class VEX_Statement(Model):
    document = ForeignKey(VEX_Document, related_name="statements", on_delete=CASCADE)
    vulnerability_id = CharField(max_length=255)
    description = TextField(max_length=2048, blank=True)
    status = CharField(max_length=24, choices=VEX_Status.VEX_STATUS_CHOICES)
    justification = CharField(max_length=64, choices=VEX_Justification.VEX_JUSTIFICATION_CHOICES, blank=True)
    impact = CharField(max_length=255, blank=True)
    remediation = CharField(max_length=255, blank=True)
    product_purl = CharField(max_length=255, blank=True)
    component_purl = CharField(max_length=255, blank=True)
    component_cyclonedx_bom_link = CharField(max_length=512, blank=True)

    class Meta:
        indexes = [
            Index(fields=["product_purl"]),
            Index(fields=["component_cyclonedx_bom_link"]),
        ]
