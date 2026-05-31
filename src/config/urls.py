"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    Django_AGGREGATE. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    Django_AGGREGATE. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    Django_AGGREGATE. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
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


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),

    path('tasks/', include('task_manager.urls')),
    path('', include('account.urls')),
]



# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('tasks/', include('task_manager.urls')),
#
#     path('', include('account.urls')),
#
#     path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
#
#     path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
#     path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
#     path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
#
#     path('api-token-auth/', views.obtain_auth_token),
#
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
#
#
#     path('api/logout/', logout_view, name='logout'),
#     path('api/token/refresh/', CustomTokenRefreshView.as_view()),
#
#
# ] + debug_toolbar_urls() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

