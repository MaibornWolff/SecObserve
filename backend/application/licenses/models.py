from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    CASCADE,
    PROTECT,
    BooleanField,
    CharField,
    ForeignKey,
    IntegerField,
    ManyToManyField,
    Model,
    TextField,
)

from application.access_control.models import User
from application.core.models import Branch, Product
from application.licenses.types import License_Policy_Evaluation_Result


class License(Model):
    spdx_id = CharField(max_length=255, unique=True)
    name = CharField(max_length=255)
    reference = TextField(max_length=2048, blank=True)
    is_osi_approved = BooleanField(null=True)
    is_deprecated = BooleanField(null=True)

    def __str__(self):
        return self.spdx_id


class License_Group(Model):
    name = CharField(max_length=255, unique=True)
    description = TextField(max_length=2048, blank=True)
    is_public = BooleanField(default=False)
    licenses = ManyToManyField(License, related_name="license_groups")
    users: ManyToManyField = ManyToManyField(
        User,
        through="License_Group_Member",
        related_name="license_groups",
        blank=True,
    )

    def __str__(self):
        return self.name


class License_Group_Member(Model):
    license_group = ForeignKey(License_Group, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)
    is_manager = BooleanField(default=False)

    class Meta:
        unique_together = (
            "license_group",
            "user",
        )

    def __str__(self):
        return f"{self.license_group} / {self.user}"


class License_Component(Model):
    identity_hash = CharField(max_length=64)

    product = ForeignKey(Product, on_delete=PROTECT)
    branch = ForeignKey(Branch, on_delete=CASCADE, null=True)
    upload_filename = CharField(max_length=255, blank=True)

    name = CharField(max_length=255)
    version = CharField(max_length=255, blank=True)
    name_version = CharField(max_length=513, blank=True)
    purl = CharField(max_length=255, blank=True)
    purl_type = CharField(max_length=16, blank=True)
    cpe = CharField(max_length=255, blank=True)
    dependencies = TextField(max_length=32768, blank=True)

    license = ForeignKey(License, on_delete=CASCADE, blank=True, null=True)
    unknown_license = CharField(max_length=255, blank=True)
    evaluation_result = CharField(
        max_length=16,
        choices=License_Policy_Evaluation_Result.RESULT_CHOICES,
        blank=True,
    )
    numerical_evaluation_result = IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.unsaved_license = ""

    def __str__(self):
        return self.name_version

    def save(self, *args, **kwargs) -> None:
        self.numerical_evaluation_result = (
            License_Policy_Evaluation_Result.NUMERICAL_RESULTS.get(
                self.evaluation_result, License_Policy_Evaluation_Result.RESULT_UNKNOWN
            )
        )
        return super().save(*args, **kwargs)


class License_Policy(Model):
    name = CharField(max_length=255, unique=True)
    description = TextField(max_length=2048, blank=True)
    is_public = BooleanField(default=False)
    users: ManyToManyField = ManyToManyField(
        User,
        through="License_Policy_Member",
        related_name="license_policies",
        blank=True,
    )

    def __str__(self):
        return self.name


class License_Policy_Item(Model):
    license_policy = ForeignKey(
        License_Policy, related_name="license_policy_items", on_delete=CASCADE
    )
    license_group = ForeignKey(License_Group, on_delete=CASCADE, blank=True, null=True)
    license = ForeignKey(License, on_delete=PROTECT, blank=True, null=True)
    unknown_license = CharField(max_length=255, blank=True)
    evaluation_result = CharField(
        max_length=16, choices=License_Policy_Evaluation_Result.RESULT_CHOICES
    )
    numerical_evaluation_result = IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)]
    )

    def save(self, *args, **kwargs) -> None:
        self.numerical_evaluation_result = (
            License_Policy_Evaluation_Result.NUMERICAL_RESULTS.get(
                self.evaluation_result, License_Policy_Evaluation_Result.RESULT_UNKNOWN
            )
        )

        return super().save(*args, **kwargs)


class License_Policy_Member(Model):
    license_policy = ForeignKey(License_Policy, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)
    is_manager = BooleanField(default=False)

    class Meta:
        unique_together = (
            "license_policy",
            "user",
        )

    def __str__(self):
        return f"{self.license_policy} / {self.user}"
