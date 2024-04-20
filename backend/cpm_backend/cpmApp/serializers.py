from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'desc', 'duration', 'succ_left', 'succ_right', 'ES', 'EF', 'LS', 'LF', 'slack', 'critical']
        depth = 1

