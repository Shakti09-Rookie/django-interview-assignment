"""library_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import LoginAPI, RegisterAPI, MemberViewAPI, MemberOpsAPI

schema_view = get_schema_view(
   openapi.Info(
      title="Library Management API",
      default_version='v1',
      description="Library management system API",
      terms_of_service="https://www.lms.com/policies/terms/",
      contact=openapi.Contact(email="shaktidagar09@gmail.com"),
      license=openapi.License(name="LMS License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',RegisterAPI.as_view(), name='register'),
    path('', include('library.urls')),
    path('members/', MemberViewAPI.as_view(), name='member-list'),
    path('members/<str:id>/', MemberOpsAPI.as_view(), name='member-operations'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginAPI.as_view(), name='login'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
