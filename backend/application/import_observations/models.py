from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    CASCADE,
    PROTECT,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Index,
    IntegerField,
    Model,
)
from encrypted_model_fields.fields import EncryptedCharField

from application.core.models import Branch, Product
from application.import_observations.types import Parser_Source, Parser_Type


class Parser(Model):
    name = CharField(max_length=255, unique=True)
    type = CharField(max_length=16, choices=Parser_Type.TYPE_CHOICES)
    source = CharField(max_length=16, choices=Parser_Source.SOURCE_CHOICES)
    module_name = CharField(max_length=255, blank=True)
    class_name = CharField(max_length=255, blank=True)

    class Meta:
        db_table = "core_parser"
        indexes = [
            Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name


class Api_Configuration(Model):
    product = ForeignKey(Product, on_delete=CASCADE)
    name = CharField(max_length=255)
    parser = ForeignKey(Parser, on_delete=PROTECT)
    base_url = CharField(max_length=255)
    project_key = CharField(max_length=255, blank=True)
    api_key = EncryptedCharField(max_length=255, blank=True)
    query = CharField(max_length=255, blank=True)
    basic_auth_enabled = BooleanField(null=True)
    basic_auth_username = CharField(max_length=255, blank=True)
    basic_auth_password = EncryptedCharField(max_length=255, blank=True)
    verify_ssl = BooleanField(null=True)

    class Meta:
        unique_together = (
            "product",
            "name",
        )


class Vulnerability_Check(Model):
    product = ForeignKey(Product, on_delete=CASCADE)
    branch = ForeignKey(Branch, on_delete=CASCADE, null=True)
    filename = CharField(max_length=255, blank=True)
    api_configuration_name = CharField(max_length=255, blank=True)
    scanner = CharField(max_length=255, blank=True)
    first_import = DateTimeField(auto_now_add=True)
    last_import = DateTimeField(auto_now=True)
    last_import_observations_new = IntegerField(
        null=True, validators=[MinValueValidator(0), MaxValueValidator(999999)]
    )
    last_import_observations_updated = IntegerField(
        null=True, validators=[MinValueValidator(0), MaxValueValidator(999999)]
    )
    last_import_observations_resolved = IntegerField(
        null=True, validators=[MinValueValidator(0), MaxValueValidator(999999)]
    )

    class Meta:
        unique_together = (
            "product",
            "branch",
            "filename",
            "api_configuration_name",
        )
