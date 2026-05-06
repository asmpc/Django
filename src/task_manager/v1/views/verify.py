from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenVerifyView as BaseTokenVerifyView



@extend_schema(tags=["api-token-auth"])
class  CustomTokenVerifyView(BaseTokenVerifyView):

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)