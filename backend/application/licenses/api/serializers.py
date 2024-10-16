from rest_framework.serializers import ModelSerializer, SerializerMethodField

from application.licenses.models import License, License_Group


class LicenseSerializer(ModelSerializer):
    is_in_license_group = SerializerMethodField()

    class Meta:
        model = License
        fields = "__all__"

    def get_is_in_license_group(self, obj:License) -> bool:
        return License_Group.objects.filter(licenses=obj).exists()

class LicenseGroupSerializer(ModelSerializer):
    class Meta:
        model = License_Group
        fields = "__all__"
