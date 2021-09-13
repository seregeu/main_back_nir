from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user and request.user.is_anonymous:
            request.user = SimpleLazyObject(lambda: self.__class__.get_jwt_user(request))

    @staticmethod
    def get_jwt_user(request):
        credentials = JSONWebTokenAuthentication().authenticate(request)
        return credentials[0] if credentials else AnonymousUser()
