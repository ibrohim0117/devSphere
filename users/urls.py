from django.urls import path
from .views import (
    RegisterView, VerifyEmailView, LogoutRedirectView,
    UserLoginView, ProfileView, ResendVerificationEmailView
)


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutRedirectView.as_view(), name="logout"),

    path("verify-email/<uuid:token>/", VerifyEmailView.as_view(), name="verify-email"),
    path("resend-verification/", ResendVerificationEmailView.as_view(), name="resend_verification"),

    path('profile/', ProfileView.as_view(), name='profile'),
]