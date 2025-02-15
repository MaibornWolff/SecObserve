from django.db.models import CharField, Model
from picklefield import PickledObjectField  # nosec B403

# picklefield is used to store python objects in the database


class Constance(Model):
    key = CharField(max_length=255, unique=True)
    value = PickledObjectField(null=True, blank=True)

    class Meta:
        verbose_name = "constance"
        verbose_name_plural = "constances"
        permissions = [
            ("change_config", "Can change config"),
            ("view_config", "Can view config"),
        ]

    def __str__(self) -> str:
        return self.key
