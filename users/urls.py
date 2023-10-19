from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import UserDetailView, user_stats, CreateUserView

app_name = "users"

urlpatterns = [
    path("users/register/", CreateUserView.as_view(), name="register"),
    path("users/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("users/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/me/", UserDetailView.as_view(), name="user-details"),
    path("users/reading_stats/", user_stats, name="reading-stats"),
]
