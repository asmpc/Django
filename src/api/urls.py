from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.static import static
from config import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView
from task_manager.v1.views.logout import logout_view
from task_manager.v1.views.refresh import CustomTokenRefreshView
from task_manager.v1.views.token import CustomTokenObtainPairView
from task_manager.v1.views.verify import CustomTokenVerifyView




urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api-token-auth/', views.obtain_auth_token),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    path('logout/', logout_view, name='logout'),
    path('token/refresh/', CustomTokenRefreshView.as_view()),
    # path("", include("task_manager.v1.urls")),
    path("", include("api.v1")),
]+ debug_toolbar_urls() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)