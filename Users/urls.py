from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    PasswordResetAPIView,
    PasswordResetConfirmAPIView,
)

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("auth/password-reset/", PasswordResetAPIView.as_view(), name="password_reset"),
    path(
        "auth/password-reset-confirm/",
        PasswordResetConfirmAPIView.as_view(),
        name="password_reset_confirm",
    ),
]
