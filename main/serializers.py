from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
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
    class Meta:
        model = Patient
        fields = ("userTransferID", "age", "height", "weight", "firstName", "lastName", "phoneNumber", "dateOfBirth",
                  "ethnicity", "race", "gender", "marital", "diet", "givenBirth", "timesBirth", "smoking", "currentPos")

    def create(self, validated_data):
        pk = validated_data.pop('userTransferID')
        loc = validated_data.pop('currentPos')
        pnt = Point(loc['lng'], loc['lat'])
        return Patient.objects.create(user=User.objects.get(id=pk), currentPos=pnt, **validated_data)


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


class ModalityResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModalityResource
        fields = ('articleLink', 'articleImage', 'title', 'description', 'publishDate', 'goal', 'typeArticle', 'patientReadScore',
                  'patientPhysicalScore', 'patientMoodScore', 'timeRequired')


class PayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payer
        fields = ('corporationName', 'applicationId', 'email', 'patient_firstName', 'patient_lastName',
                  'patient_email', 'patient_phoneNumber', 'patient_dateOfBirth', 'patient_gender', 'patient_race','patient_age')

    patient_firstName = serializers.SerializerMethodField('get_patient_firstName')
    patient_lastName = serializers.SerializerMethodField('get_patient_lastName')
    patient_email = serializers.SerializerMethodField('get_patient_email')
    patient_phoneNumber = serializers.SerializerMethodField('get_patient_phoneNumber')
    patient_dateOfBirth = serializers.SerializerMethodField('get_patient_dateOfBirth')
    patient_gender = serializers.SerializerMethodField('get_patient_gender')
    patient_race = serializers.SerializerMethodField('get_patient_race')
    patient_age = serializers.SerializerMethodField('get_patient_age')

    def get_patient_firstName(self, obj):
        return obj.patient.firstName

    def get_patient_lastName(self, obj):
        return obj.patient.lastName

    def get_patient_email(self, obj):
        return obj.patient.email

    def get_patient_phoneNumber(self, obj):
        return obj.patient.phoneNumber

    def get_patient_dateOfBirth(self, obj):
        return obj.patient.dateOfBirth

    def get_patient_gender(self, obj):
        return obj.patient.gender

    def get_patient_race(self, obj):
        return obj.patient.race

    def get_patient_age(self, obj):
        return obj.patient.age

