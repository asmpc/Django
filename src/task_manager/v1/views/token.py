from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView as BaseTokenObtainPairView



@extend_schema(tags=["api-token-auth"])
class CustomTokenObtainPairView(BaseTokenObtainPairView):

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)