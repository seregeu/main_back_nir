from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from app_api.models import AppApi
from app_api.serializers import AppApiSerializer


class AppAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = AppApi.objects.all()
        serializer = AppApiSerializer(query, many=True)
        return Response({"apps": serializer.data})
# Create your views here.
