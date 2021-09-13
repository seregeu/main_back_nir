import django.contrib.auth.password_validation as validators
from django.contrib.auth.models import User
from django.core import exceptions
from rest_framework import serializers

from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('phone', )


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'profile')


class ModifyUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('profile', )


class RegisterUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, min_length=6)
    first_name = serializers.CharField(required=True, min_length=3)
    last_name = serializers.CharField(required=True, min_length=4)
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.CharField(write_only=True, required=True)

    phone = serializers.CharField(write_only=True, required=True, min_length=10)

    def validate_username(self, value):
        if User.objects.filter(username=value).first():
            raise serializers.ValidationError('Username is already in use.')

        return value

    def validate_password(self, value):
        user = User(username=self.initial_data.get('username'))

        try:
            validators.validate_password(password=value, user=user)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(e.messages)

        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        phone = validated_data.pop('phone', None)

        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()

        instance.profile.phone = phone
        instance.profile.save()

        return instance

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'phone')
