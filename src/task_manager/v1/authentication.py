from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.cache import cache
from rest_framework.exceptions import AuthenticationFailed



class CustomJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        token = super().get_validated_token(raw_token)

        jti = token.get("jti")

        if jti and cache.get(f"blacklist:{jti}"):
            raise AuthenticationFailed("Token is blacklisted")

        return token