from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'date_joined')

    def create(self, validated_data):
        password = make_password(validated_data.pop('password'))
        return User.objects.create(password=password, **validated_data)


class PatientSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField()
    class Meta:
        model = Patient
        fields = ('user_id', 'age', 'height', 'weight')

    def create(self, validated_data):
        pk = validated_data.pop('user_id')
        return Patient.objects.create(user=User.objects.get(id=pk), **validated_data)


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'username': user.username,
            'token': jwt_token
        }