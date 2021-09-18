from django.urls import path

from actions_api.views import ActionAPIView, CommentAPIView

urlpatterns = [
    path('add/', ActionAPIView.as_view()),
    path('comment/<int:pk>/', CommentAPIView.as_view()),
]
