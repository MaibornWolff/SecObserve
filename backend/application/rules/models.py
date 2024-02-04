from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    ForeignKey,
    Index,
    Model,
    TextField,
)

from application.core.models import Parser, Product
from application.core.types import Severity, Status


class Rule(Model):
    name = CharField(max_length=255)
    description = TextField(max_length=2048, blank=True)
    product = ForeignKey(Product, blank=True, null=True, on_delete=CASCADE)
    parser = ForeignKey(Parser, null=True, on_delete=CASCADE)
    scanner_prefix = CharField(max_length=255, blank=True)
    title = CharField(max_length=255, blank=True)
    description_observation = CharField(max_length=255, blank=True)
    origin_component_name_version = CharField(max_length=513, blank=True)
    origin_docker_image_name_tag = CharField(max_length=513, blank=True)
    origin_endpoint_url = TextField(max_length=2048, blank=True)
    origin_service_name = CharField(max_length=255, blank=True)
    origin_source_file = CharField(max_length=255, blank=True)
    origin_cloud_qualified_resource = CharField(max_length=255, blank=True)
    new_severity = CharField(
        max_length=12, choices=Severity.SEVERITY_CHOICES, blank=True
    )
    new_status = CharField(max_length=16, choices=Status.STATUS_CHOICES, blank=True)
    enabled = BooleanField(default=True)

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
