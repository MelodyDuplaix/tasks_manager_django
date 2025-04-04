from django.contrib.auth.models import User
from rest_framework import serializers
from tasks.models import SubManager

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
