from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    IntegerField,
    Model,
    OneToOneField,
    TextField,
)

from application.core.models import Product
from application.vex.types import CSAF_Publisher_Category, CSAF_Tracking_Status


class VEX_Base(Model):
    product = OneToOneField(Product, on_delete=CASCADE, null=True)
    vulnerability_name = CharField(max_length=255, blank=True)
    document_base_id = CharField(max_length=36, unique=True)
    document_id = CharField(max_length=255)
    version = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)])
    content_hash = CharField(max_length=256, blank=True)

    class Meta:
        abstract = True


class OpenVEX(VEX_Base):
    author = CharField(max_length=255)
    role = CharField(max_length=255, blank=True)
    timestamp = DateTimeField(auto_now_add=True)
    last_updated = DateTimeField(auto_now=True)

class OpenVEX_Vulnerability(Model):
    openvex = ForeignKey(OpenVEX, related_name="vulnerability_names", on_delete=CASCADE)
    name = CharField(max_length=255)

class CSAF(VEX_Base):
    title = CharField(max_length=255)
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


class CSAF_Revision(Model):
    csaf = ForeignKey(CSAF, related_name="revisions", on_delete=CASCADE)
    date = DateTimeField()
    version = IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(999999)]
    )
    summary = TextField(max_length=255)
