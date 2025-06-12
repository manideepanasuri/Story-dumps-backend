from rest_framework import serializers

from makevideo.models import TaskModel, BackGroundModel, VoiceModel


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = '__all__'

class BackGroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackGroundModel
        fields = '__all__'
class VoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceModel
        fields = '__all__'