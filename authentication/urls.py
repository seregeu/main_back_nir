from django.urls import path

from .views import UserRegisterView, UserProfileAPIView

urlpatterns = [
    path('register/', UserRegisterView.as_view()),
    path('profile/', UserProfileAPIView.as_view()),
]
