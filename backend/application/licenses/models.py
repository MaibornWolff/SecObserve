from django.db.models import (
    CASCADE,
    PROTECT,
    BooleanField,
    CharField,
    ForeignKey,
    ManyToManyField,
    Model,
    TextField,
)

from application.access_control.models import User
from application.import_observations.models import Vulnerability_Check
from application.licenses.types import License_Policy_Evaluation_Result


class License(Model):
    license_id = CharField(max_length=255, unique=True)
    name = CharField(max_length=255)
    reference = TextField(max_length=2048, blank=True)
    is_osi_approved = BooleanField(null=True)
    is_deprecated = BooleanField(null=True)

    def __str__(self):
        return self.license_id


class License_Group(Model):
    name = CharField(max_length=255)
    description = TextField(max_length=2048, blank=True)
    licenses = ManyToManyField(License, related_name="license_groups")

    def __str__(self):
        return self.name


class Component(Model):
    vulnerability_check = ForeignKey(Vulnerability_Check, on_delete=CASCADE)
    name = CharField(max_length=255)
    version = CharField(max_length=255, blank=True)
    name_version = CharField(max_length=513, blank=True)
    purl = CharField(max_length=255, blank=True)
    purl_type = CharField(max_length=16, blank=True)
    cpe = CharField(max_length=255, blank=True)
    dependencies = TextField(max_length=32768, blank=True)
    license = ForeignKey(License, on_delete=CASCADE, null=True)
    unknown_license = CharField(max_length=255, blank=True)
    license_policy_evalution_result = CharField(
        max_length=16,
        choices=License_Policy_Evaluation_Result.RESULT_CHOICES,
        default=License_Policy_Evaluation_Result.RESULT_UNKOWN,
    )

    def __str__(self):
        return self.name_version


class License_Policy(Model):
    name = CharField(max_length=255)
    description = TextField(max_length=2048, blank=True)
    users: ManyToManyField = ManyToManyField(
        User,
        through="License_Policy_Member",
        related_name="license_policies",
        blank=True,
    )

    def __str__(self):
        return self.name


class License_Policy_Item(Model):
    license_policy = ForeignKey(License_Policy, on_delete=CASCADE)
    license_group = ForeignKey(License_Group, on_delete=CASCADE, null=True)
    license = ForeignKey(License, on_delete=PROTECT, null=True)
    unknown_license = CharField(max_length=255, blank=True)
    evaluation_result = CharField(
        max_length=16, choices=License_Policy_Evaluation_Result.RESULT_CHOICES
    )


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
