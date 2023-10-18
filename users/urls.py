from django.urls import path

from users.views import UserDetailView, user_stats

app_name = "users"

urlpatterns = [
    path("users/me/", UserDetailView.as_view(), name="user-details"),
    path("users/reading_stats/", user_stats, name="reading-stats"),
]
