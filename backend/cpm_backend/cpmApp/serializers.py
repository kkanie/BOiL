from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'duration', 'ES', 'EF', 'LS', 'LF', 'slack', 'is_critical']
        depth = 1

    def validate_duration(self, value):
        # zeby cyferki byly na pewno
        if not isinstance(value, str) or not value.isdigit():
            raise serializers.ValidationError("Duration must be a number represented as a string.")
        return value

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        if 'duration' in ret:
            ret['duration'] = int(ret['duration'])
        return ret

from rest_framework import serializers
from .models import Activity

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'is_critical', 'is_start', 'is_end', 'ES', 'EF', 'LS', 'LF', 'slack']

