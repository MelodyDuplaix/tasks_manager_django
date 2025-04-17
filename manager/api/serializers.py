from django.contrib.auth.models import User
from rest_framework import serializers
from tasks.models import SubManager, Task, PonctualTask, Reward, TaskType, Action
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data

class SubManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubManager
        fields = ['id', 'name', 'daily_objectif', 'yearly_objectif', 'active']

class TaskTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskType
        fields = ['id', 'name']

class TaskSerializer(serializers.ModelSerializer):
    type = TaskTypeSerializer()
    done_today_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'name', 'coins_number', 'type', 'done_today_count']

    def get_done_today_count(self, obj):
        return Action.objects.filter(
            type=obj.type,
            sub_manager=obj.type.sub_manager,
            date__date=timezone.now().date()
        ).count()
        
class PonctualTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = PonctualTask
        fields = ['id', 'name', 'coins_number', 'date']

class RewardSerializer(serializers.ModelSerializer):
    sub_manager_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Reward
        fields = ['id', 'name', 'coins_number', 'sub_manager_id']
