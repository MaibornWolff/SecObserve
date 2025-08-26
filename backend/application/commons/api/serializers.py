from rest_framework.serializers import (
    CharField,
    IntegerField,
    ListField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
)

from application.commons.models import Settings


class VersionSerializer(Serializer):
    version = CharField(max_length=200)


class StatusSettingsSerializer(Serializer):
    features = ListField(child=CharField(), min_length=0, max_length=200, required=True)
    risk_acceptance_expiry_days = IntegerField()
    vex_justification_style = CharField()


class SettingsSerializer(ModelSerializer):
    id = SerializerMethodField()

    class Meta:
        model = Settings
        fields = "__all__"

    def get_id(self, obj: Settings) -> int:  # pylint: disable=unused-argument
        # obj is needed for the signature but we don't need it
        # The id is hardcoded to 1 because there is only one instance of the Settings model
        return 1
