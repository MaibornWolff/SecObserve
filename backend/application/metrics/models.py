from django.db.models import (
    CASCADE,
    DateField,
    DateTimeField,
    ForeignKey,
    IntegerField,
    Model,
)
from django.utils import timezone

from application.core.models import Product


class Product_Metrics(Model):
    product = ForeignKey(Product, on_delete=CASCADE)
    date = DateField()

    open_critical = IntegerField(default=0)
    open_high = IntegerField(default=0)
    open_medium = IntegerField(default=0)
    open_low = IntegerField(default=0)
    open_none = IntegerField(default=0)
    open_unknown = IntegerField(default=0)

    open = IntegerField(default=0)
    resolved = IntegerField(default=0)
    duplicate = IntegerField(default=0)
    false_positive = IntegerField(default=0)
    in_review = IntegerField(default=0)
    not_affected = IntegerField(default=0)
    not_security = IntegerField(default=0)
    risk_accepted = IntegerField(default=0)

    class Meta:
        unique_together = (
            "product",
            "date",
        )


class Product_Metrics_Status(Model):
    last_calculated = DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls) -> "Product_Metrics_Status":
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
