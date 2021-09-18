from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from actions_api.models import Action
from actions_api.serializers import ActionAPISerializer


class ActionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ActionAPISerializer(data=request.data)
        if serializer.is_valid():
            Action.objects.create(**serializer.data, user=request.user)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_200_OK)
# Create your views here.
