from rest_framework.serializers import ModelSerializer

from application.background_tasks.models import Periodic_Task


class PeriodicTaskSerializer(ModelSerializer):
    class Meta:
        model = Periodic_Task
        fields = "__all__"
