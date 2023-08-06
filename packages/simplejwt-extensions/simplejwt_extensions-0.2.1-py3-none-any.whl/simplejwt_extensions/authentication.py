from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.authentication import JWTAuthentication as SimpleJWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.state import User

from .settings import api_settings


class JWTAuthentication(SimpleJWTAuthentication):
    def authenticate(self, request):
        self.request = request
        return super().authenticate(request)

    def get_user(self, validated_token):
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken(_('Token contained no recognizable user identification'))

        try:
            user = User.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except User.DoesNotExist:
            user = None
            if api_settings.NEW_USER_CALLBACK:
                user = api_settings.NEW_USER_CALLBACK(self.request, user_id)
            if user is None:
                raise AuthenticationFailed(_('User not found'), code='user_not_found')

        if not user.is_active:
            raise AuthenticationFailed(_('User is inactive'), code='user_inactive')

        return user
