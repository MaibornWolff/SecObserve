from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    TextField,
    BooleanField,
    CASCADE,
)

from application.core.models import Product, Parser, Observation


class Rule(Model):
    name = CharField(max_length=255)
    description = TextField(max_length=2048, blank=True)
    product = ForeignKey(Product, blank=True, null=True, on_delete=CASCADE)
    parser = ForeignKey(Parser, on_delete=CASCADE)
    scanner_prefix = CharField(max_length=255, blank=True)
    title = CharField(max_length=255, blank=True)
    origin_component_name_version = CharField(max_length=513, blank=True)
    origin_docker_image_name_tag = CharField(max_length=513, blank=True)
    origin_endpoint_url = TextField(max_length=2048, blank=True)
    origin_service_name = CharField(max_length=255, blank=True)
    origin_source_file = CharField(max_length=255, blank=True)
    new_severity = CharField(
        max_length=12, choices=Observation.SEVERITY_CHOICES, blank=True
    )
    new_status = CharField(
        max_length=16, choices=Observation.STATUS_CHOICES, blank=True
    )
    enabled = BooleanField(default=True)

    class Meta:
        unique_together = (
            "product",
            "name",
        )

    def __str__(self):
        return self.name
