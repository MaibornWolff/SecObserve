from rest_framework.serializers import CharField, Serializer


class VersionSerializer(Serializer):
    version = CharField(max_length=200)
