from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from rest_framework.exceptions import AuthenticationFailed


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")

        token = RefreshToken(refresh_token)
        jti = token["jti"]

        if cache.get(f"blacklist:{jti}"):
            raise AuthenticationFailed("Token is blacklisted")

        return super().post(request, *args, **kwargs)