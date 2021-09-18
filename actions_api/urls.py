from django.urls import path

from actions_api.views import ActionAPIView

urlpatterns = [
    path('add/', ActionAPIView.as_view()),
]