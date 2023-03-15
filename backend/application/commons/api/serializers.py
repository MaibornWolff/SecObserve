from rest_framework.serializers import CharField, Serializer


class CommitSerializer(Serializer):
    commit_id = CharField(max_length=200)
