import django.contrib.auth.password_validation as validators
from django.contrib.auth.models import User
from django.core import exceptions
from rest_framework import serializers

from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('phone', 'gender',
                  'second_mail', 'img_url', 'cards', 'bot')


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
    second_mail = serializers.CharField(write_only=True, required=False, default="", allow_blank=True)
    cards = serializers.CharField(write_only=True, required=False, default="", allow_blank=True)
    gender = serializers.CharField(write_only=True, required=False)
    phone = serializers.CharField(write_only=True, required=True, min_length=10)
    img_url = serializers.CharField(write_only=True, required=False, max_length=200, default="", allow_blank=True)
    bot = serializers.BooleanField(required=False)

    def validate_username(self, value):
        if User.objects.filter(username=value).first():
            raise serializers.ValidationError('Username is already in use.')

        return value

    def validate_password(self, value):
        user = User(username=self.initial_data.get('username'))
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        phone = validated_data.pop('phone', None)
        gender = validated_data.pop('gender', None)
        second_mail = validated_data.pop('second_mail', None)
        try:
            cards = validated_data.pop('cards', None)
        except:
            cards = ""
        img_url = validated_data.pop('img_url', None)
        bot = validated_data.pop('bot', None)
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()

        instance.profile.phone = phone
        instance.profile.gender = gender
        instance.profile.second_mail = second_mail
        instance.profile.cards = cards
        instance.profile.img_url = img_url
        instance.profile.bot = bot
        instance.profile.save()

        return instance

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'phone', 'gender',
                  'second_mail', 'cards', 'img_url', 'bot')
