from django.urls import path


from app_api.views import AppAPIView

urlpatterns = [
    path('list/', AppAPIView.as_view()),
]