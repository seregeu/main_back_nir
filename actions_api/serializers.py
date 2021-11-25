from django.contrib.auth.models import User
from rest_framework import serializers

from authentication.serializers import UserProfileSerializer


class ActionAPISerializer(serializers.Serializer):
    app_id = serializers.IntegerField()
    data = serializers.CharField(max_length=200, default="", allow_blank=True)
    action_type = serializers.ChoiceField(choices=[1, 2, 3, 4, 5], required=True)

class ActionAPIWithUserSerializer(serializers.Serializer):
    app_id = serializers.IntegerField()
    date = serializers.DateTimeField()
    data = serializers.CharField(max_length=200, default="")
    action_type = serializers.ChoiceField(choices=[1, 2, 3, 4, 5], required=True)
    user = serializers.CharField(max_length=200, default="")

class CommentAPISerializer(serializers.Serializer):
    content = serializers.CharField(max_length=200)
    username = serializers.CharField(max_length=100)
    user = UserProfileSerializer()
