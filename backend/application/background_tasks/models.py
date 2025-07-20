from datetime import date
from decimal import Decimal
from typing import Any

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import BooleanField, CharField, DateField, DecimalField, Model


class EPSS_Score(Model):
    cve = CharField(max_length=255, unique=True)
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

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args: Any, **kwargs: Any) -> tuple[int, dict[str, int]]:
        return 0, {}

    @classmethod
    def load(cls) -> "EPSS_Status":
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Exploit_Information(Model):
    cve = CharField(max_length=255, unique=True)
    base_cvss_vector = CharField(max_length=255, blank=True)
    cisa_kev = BooleanField(default=False)
    vulncheck_kev = BooleanField(default=False)
    exploitdb = BooleanField(default=False)
    metasploit = BooleanField(default=False)
    nuclei = BooleanField(default=False)
    poc_github = BooleanField(default=False)
