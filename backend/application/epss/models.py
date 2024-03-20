from datetime import date
from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import CharField, DateField, DecimalField, Model


class EPSS_Score(Model):
    cve = CharField(max_length=20, unique=True)
    epss_score = DecimalField(
        max_digits=6,
        decimal_places=5,
        null=True,
        validators=[MinValueValidator(Decimal(0)), MaxValueValidator(Decimal(1))],
    )
    epss_percentile = DecimalField(
        max_digits=6,
        decimal_places=5,
        null=True,
        validators=[MinValueValidator(Decimal(0)), MaxValueValidator(Decimal(1))],
    )


class EPSS_Status(Model):
    score_date = DateField(default=date.today)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls) -> "EPSS_Status":
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
