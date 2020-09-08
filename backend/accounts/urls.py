from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import (
    SignUpView, LoginView,
    LogOutView, MobileTokenView,
    UserInfoView)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', jwt_views.TokenObtainPairView.as_view(),
         name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('refresh-token/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('user-info/<int:pk>/', UserInfoView.as_view(),
         name='user-info'),
    path('mobile-token/', MobileTokenView.as_view(),
         name='mobile-token')
]