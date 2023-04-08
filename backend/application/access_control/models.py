from django.contrib.auth.models import AbstractUser
from django.db.models import CASCADE, BooleanField, CharField, Model, OneToOneField
from encrypted_model_fields.fields import EncryptedCharField


class User(AbstractUser):
    THEME_LIGHT = "light"
    THEME_DARK = "dark"

    THEME_CHOICES = [
        (THEME_LIGHT, THEME_LIGHT),
        (THEME_DARK, THEME_DARK),
    ]

    full_name = CharField(max_length=301, blank=True)
    is_external = BooleanField(default=False)
    setting_theme = CharField(max_length=5, choices=THEME_CHOICES, default=THEME_LIGHT)

    def save(self, *args, **kwargs):
        if self.first_name and self.last_name:
            self.full_name = f"{self.first_name} {self.last_name}"
        elif self.first_name:
            self.full_name = self.first_name
        elif self.last_name:
            self.full_name = self.last_name
        else:
            self.full_name = self.username

        super(User, self).save(*args, **kwargs)


class JWT_Secret(Model):
    secret = EncryptedCharField(max_length=255)

    class Meta:
        verbose_name = "JWT secret"


class API_Token(Model):
    user = OneToOneField(User, on_delete=CASCADE, primary_key=True)
    api_token_hash = CharField(max_length=255)

    class Meta:
        verbose_name = "API token"
        verbose_name_plural = "API token"
