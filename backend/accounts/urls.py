from django.urls import path
from .views import (
    RegisterAPIView,
    VerifyCodeAPIView,
    ResendCodeAPIView,
    LoginAPIView,
    PasswordResetRequestAPIView,
    PasswordResetConfirmAPIView,
    CurrentUserAPIView,
    ChangePasswordAPIView,
    LogoutAPIView,
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='auth-register'),
    path('verify-code/', VerifyCodeAPIView.as_view(), name='auth-verify-code'),
    path('resend-code/', ResendCodeAPIView.as_view(), name='auth-resend-code'),
    path('login/', LoginAPIView.as_view(), name='auth-login'),
    path('password-reset/request/', PasswordResetRequestAPIView.as_view(), name='auth-reset-request'),
    path('password-reset/confirm/', PasswordResetConfirmAPIView.as_view(), name='auth-reset-confirm'),
    path('me/', CurrentUserAPIView.as_view(), name='auth-me'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='auth-change-password'),
    path('logout/', LogoutAPIView.as_view(), name='auth-logout'),
]

