from typing import TypedDict

from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    FileField,
    IntegerField,
    CharField,
    BooleanField,
    ValidationError,
)
from django.core.validators import MinValueValidator

from application.access_control.services.roles_permissions import Permissions
from application.core.api.serializers import NestedProductSerializer
from application.import_observations.models import Api_Configuration
from application.import_observations.services.import_observations import (
    api_check_connection,
)


class FileUploadObservationsByIdRequestSerializer(Serializer):
    file = FileField(max_length=255)
    product = IntegerField(validators=[MinValueValidator(0)])
    parser = IntegerField(validators=[MinValueValidator(0)])
    service = CharField(max_length=255, required=False)
    docker_image_name_tag = CharField(max_length=513, required=False)
    endpoint_url = CharField(max_length=2048, required=False)


class FileUploadObservationsByNameRequestSerializer(Serializer):
    file = FileField(max_length=255)
    product_name = CharField(max_length=255)
    parser_name = CharField(max_length=255)
    service = CharField(max_length=255, required=False)
    docker_image_name_tag = CharField(max_length=513, required=False)
    endpoint_url = CharField(max_length=2048, required=False)


class ApiImportObservationsByIdRequestSerializer(Serializer):
    api_configuration = IntegerField(validators=[MinValueValidator(0)])
    service = CharField(max_length=255, required=False, allow_blank=True)
    docker_image_name_tag = CharField(max_length=513, required=False, allow_blank=True)
    endpoint_url = CharField(max_length=2048, required=False, allow_blank=True)


class ApiImportObservationsByNameRequestSerializer(Serializer):
    api_configuration_name = CharField(max_length=255)
    service = CharField(max_length=255, required=False)
    docker_image_name_tag = CharField(max_length=513, required=False)
    endpoint_url = CharField(max_length=2048, required=False)


class ImportObservationsResponseSerializer(Serializer):
    observations_new = IntegerField()
    observations_updated = IntegerField()
    observations_resolved = IntegerField()


class ApiConfigurationSerializer(ModelSerializer):
    product_data = NestedProductSerializer(source="product", read_only=True)
    test_connection = BooleanField(write_only=True, required=False, default=False)

    class Meta:
        model = Api_Configuration
        fields = "__all__"

    def to_representation(self, obj):
        # Only users who can edit an API Configuration are allowed to see the API key
        data = super(ApiConfigurationSerializer, self).to_representation(obj)

        permissions = data.get("product_data", {}).get("permissions", [])
        if Permissions.Api_Configuration_Edit not in permissions:
            data.pop("api_key")

        return data

    def validate(self, data: dict):
        self.instance: Api_Configuration
        if data.pop("test_connection", False):
            if self.instance is not None:
                product = data.get("product", self.instance.product)
                name = data.get("name", self.instance.name)
                parser = data.get("parser", self.instance.parser)
                base_url = data.get("base_url", self.instance.base_url)
                project_key = data.get("project_key", self.instance.project_key)
                api_key = data.get("api_key", self.instance.api_key)
            else:
                product = data.get("product")
                name = data.get("name")
                parser = data.get("parser")
                base_url = data.get("base_url")
                project_key = data.get("project_key")
                api_key = data.get("api_key")

            api_configuration = Api_Configuration(
                product=product,
                name=name,
                parser=parser,
                base_url=base_url,
                project_key=project_key,
                api_key=api_key,
            )
            valid, errors = api_check_connection(api_configuration)
            if not valid:
                raise ValidationError("\n".join(errors))

        data_product = data.get("product")
        if (
            self.instance is not None
            and data_product
            and data_product != self.instance.product
        ):
            raise ValidationError("Product cannot be changed")

        return data
