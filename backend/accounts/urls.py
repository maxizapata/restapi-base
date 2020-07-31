from django.contrib import admin
from django.urls import path, include
from .views import (
    SignUpView, LoginView,
    LogOutView, MobileTokenView,
    UserInfoView)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('user-info/<int:pk>/', UserInfoView.as_view(),
         name='user-info'),
    path('mobile-token/', MobileTokenView.as_view(),
         name='mobile-token')
]