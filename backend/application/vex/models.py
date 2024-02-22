from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    CASCADE,
    PROTECT,
    CharField,
    DateTimeField,
    ForeignKey,
    IntegerField,
    Model,
    OneToOneField,
    TextField,
)

from application.core.models import Product
from application.vex.types import CSAF_Role, CSAF_Status


class Vulnerability(Model):
    name = CharField(max_length=255, unique=True)
    description = TextField(max_length=2048, blank=True)
    recommendation = TextField(max_length=2048, blank=True)


class VEX_Base(Model):
    product = OneToOneField(Product, on_delete=CASCADE, null=True)
    vulnerability = ForeignKey(Vulnerability, on_delete=PROTECT, null=True)
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


class CSAF(VEX_Base):
    title = CharField(max_length=255)
    tracking_initial_release_date = DateTimeField(auto_now_add=True)
    tracking_current_release_date = DateTimeField(auto_now=True)
    tracking_status = CharField(max_length=16, choices=CSAF_Status.CSAF_STATUS_CHOICES)
    publisher_name = CharField(max_length=255)
    publisher_category = CharField(max_length=16, choices=CSAF_Role.CSAF_ROLE_CHOICES)
    publisher_namespace = CharField(max_length=255)
