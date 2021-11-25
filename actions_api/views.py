from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from actions_api.models import Action
from actions_api.serializers import ActionAPISerializer, CommentAPISerializer, ActionAPIWithUserSerializer
from authentication.models import UserProfile

from pandas import DataFrame
from bot_detected.data import Data


class ActionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ActionAPISerializer(data=request.data)
        if serializer.is_valid():
            Action.objects.create(**serializer.data, user=request.user)

            print("Action from", request.user.id)
            if not len(user_activity := list(Action.objects.filter(user=request.user.id).values())) % 2:
                print('% 10 == 0!')
                data = Data(act=DataFrame(user_activity),
                            users=DataFrame(list(UserProfile.objects.filter(user=request.user.id).values())))
                data.data_preparation()
                data.bot_detected()
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_200_OK)


class Comment:
    def __init__(self, user, content):
        self.user = user
        self.content = content
        self.username = user.user.username

    def __str__(self):
        return f"content: {self.content} " \
               f"username:{self.username}" \
               f"user: {self.user} "


class CommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        queryset = Action.objects.all().filter(app_id=pk, action_type=1)
        print(queryset)
        serializer_actions = ActionAPIWithUserSerializer(queryset, many=True)
        comment_list = []
        for data_act in serializer_actions.data:
            print(data_act)
            user = get_object_or_404(User, username=data_act['user'])
            user_profile = get_object_or_404(UserProfile, user=user)
            comment = Comment(user=user_profile, content=data_act['data'])
            comment_list.append(comment)
        print(comment_list)
        serializer = CommentAPISerializer(comment_list, many=True)

        return Response(data={'comments': serializer.data})

# Create your views here.
