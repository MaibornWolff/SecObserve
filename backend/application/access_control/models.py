from typing import Any

from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    ForeignKey,
    Index,
    ManyToManyField,
    Model,
    OneToOneField,
    TextField,
)
from encrypted_model_fields.fields import EncryptedCharField


class User(AbstractUser):
    THEME_LIGHT = "light"
    THEME_DARK = "dark"

    THEME_CHOICES = [
        (THEME_LIGHT, THEME_LIGHT),
        (THEME_DARK, THEME_DARK),
    ]

    LIST_SIZE_SMALL = "small"
    LIST_SIZE_MEDIUM = "medium"

    LIST_SIZE_CHOICES = [
        (LIST_SIZE_SMALL, LIST_SIZE_SMALL),
        (LIST_SIZE_MEDIUM, LIST_SIZE_MEDIUM),
    ]

    PACKAGE_INFO_PREFERENCE_DEPS_DEV = "open/source/insights"
    PACKAGE_INFO_PREFERENCE_ECOSYSTE_MS = "ecosyste.ms"

    PACKAGE_INFO_PREFERENCE_CHOICES = [
        (PACKAGE_INFO_PREFERENCE_DEPS_DEV, PACKAGE_INFO_PREFERENCE_DEPS_DEV),
        (PACKAGE_INFO_PREFERENCE_ECOSYSTE_MS, PACKAGE_INFO_PREFERENCE_ECOSYSTE_MS),
    ]

    full_name = CharField(max_length=301, blank=True)
    is_external = BooleanField(default=False)
    setting_theme = CharField(max_length=5, choices=THEME_CHOICES, default=THEME_LIGHT)
    setting_list_size = CharField(max_length=6, choices=LIST_SIZE_CHOICES, default=LIST_SIZE_MEDIUM)
    setting_package_info_preference = CharField(
        max_length=20,
        choices=PACKAGE_INFO_PREFERENCE_CHOICES,
        default=PACKAGE_INFO_PREFERENCE_DEPS_DEV,
    )
    setting_list_properties = TextField(max_length=2048, blank=True)
    oidc_groups_hash = CharField(max_length=64, blank=True)
    is_oidc_user = BooleanField(default=False)

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.first_name and self.last_name:
            self.full_name = f"{self.first_name} {self.last_name}"
        elif self.first_name:
            self.full_name = self.first_name
        elif self.last_name:
            self.full_name = self.last_name
        elif not self.full_name:
            self.full_name = self.username

        super().save(*args, **kwargs)


class Authorization_Group(Model):
    name = CharField(max_length=255, unique=True)
    oidc_group = CharField(max_length=255, blank=True)
    users: ManyToManyField = ManyToManyField(
        User,
        through="Authorization_Group_Member",
        related_name="authorization_groups",
        blank=True,
    )

    class Meta:
        verbose_name = "Authorization Group"
        verbose_name_plural = "Authorization Groups"
        indexes = [
            Index(fields=["oidc_group"]),
        ]

    def __str__(self) -> str:
        return self.name


class Authorization_Group_Member(Model):
    authorization_group = ForeignKey(Authorization_Group, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)
    is_manager = BooleanField(default=False)

    class Meta:
        unique_together = (
            "authorization_group",
            "user",
        )

    def __str__(self) -> str:
        return f"{self.authorization_group} / {self.user}"


class JWT_Secret(Model):
    secret = EncryptedCharField(max_length=255)

    class Meta:
        verbose_name = "JWT secret"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """
        Save object to the database. Removes all other entries if there
        are any.
        """
        self.__class__.objects.exclude(id=self.pk).delete()
        super().save(*args, **kwargs)

    @classmethod
    def load(cls) -> "JWT_Secret":
        """
        Load object from the database. Failing that, create a new empty
        (default) instance of the object and return it (without saving it
        to the database).
        """
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


class API_Token(Model):
    user = OneToOneField(User, on_delete=CASCADE, primary_key=True)
    api_token_hash = CharField(max_length=255)

    class Meta:
        verbose_name = "API token"
        verbose_name_plural = "API token"
