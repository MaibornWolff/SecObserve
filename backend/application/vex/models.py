from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    IntegerField,
    Model,
    TextField,
)

from application.access_control.models import User
from application.core.models import Branch, Product
from application.vex.types import (
    CSAF_Publisher_Category,
    CSAF_TLP_Label,
    CSAF_Tracking_Status,
)


class VEX_Counter(Model):
    document_id_prefix = CharField(max_length=255)
    year = IntegerField(validators=[MinValueValidator(2000), MaxValueValidator(9999)])
    counter = IntegerField(default=0)

    class Meta:
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
    timestamp = DateTimeField(auto_now_add=True)
    last_updated = DateTimeField(auto_now=True)


class OpenVEX_Branch(Model):
    openvex = ForeignKey(OpenVEX, related_name="branches", on_delete=CASCADE)
    branch = ForeignKey(Branch, related_name="openvexes", on_delete=CASCADE)


class OpenVEX_Vulnerability(Model):
    openvex = ForeignKey(OpenVEX, related_name="vulnerability_names", on_delete=CASCADE)
    name = CharField(max_length=255)


class CSAF(VEX_Base):
    title = CharField(max_length=255)
    tlp_label = CharField(max_length=16, choices=CSAF_TLP_Label.CSAF_TLP_LABEL_CHOICES)
    tracking_initial_release_date = DateTimeField(auto_now_add=True)
    tracking_current_release_date = DateTimeField(auto_now=True)
    tracking_status = CharField(
        max_length=16, choices=CSAF_Tracking_Status.CSAF_TRACKING_STATUS_CHOICES
    )
    publisher_name = CharField(max_length=255)
    publisher_category = CharField(
        max_length=16, choices=CSAF_Publisher_Category.CSAF_PUBLISHER_CATEGORY_CHOICES
    )
    publisher_namespace = CharField(max_length=255)


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
