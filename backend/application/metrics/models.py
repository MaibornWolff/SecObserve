from django.db.models import CASCADE, DateField, ForeignKey, IntegerField, Model

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
