import time
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from drf_spectacular.utils import extend_schema



@extend_schema(
    tags=["api-token-auth"],
    summary="Logout user (blacklist refresh token)",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "refresh": {"type": "string"}
            },
            "required": ["refresh"]
        }
    },
    responses={205: None}
)
@api_view(["POST"])
def logout_view(request):
    try:
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"error": "No token provided"}, status=400)

        token = RefreshToken(refresh_token)

        jti = token["jti"]
        exp = token["exp"]


        ttl = exp - int(timezone.now().timestamp())

        # защита от отрицательного ttl
        if ttl > 0:
            cache.set(f"blacklist:{jti}", "true", timeout=ttl)

        return Response({"message": "Logged out"}, status=205)

    except Exception as e:
        return Response({"error": str(e)}, status=400)


