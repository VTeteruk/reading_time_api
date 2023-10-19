from datetime import timedelta

from users.tasks import collect_user_reading_stats

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture()
def created_user() -> User:
    return get_user_model().objects.create_user(
        username="test_user",
        first_name="test",
        last_name="test",
        password="test_password",
    )


@pytest.fixture()
def authenticated_user(create_user) -> APIClient:
    client = APIClient()
    client.force_authenticate(user=create_user)
    return client


@pytest.mark.django_db
def test_create_user(client) -> None:
    url = reverse("users:register")
    data = {
        "username": "test_user",
        "email": "testuser@example.com",
        "password": "test_password",
        "first_name": "Test",
        "last_name": "User",
    }
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    user = get_user_model().objects.get(username=data["username"])
    assert user is not None
    assert user.first_name == "Test"


@pytest.mark.django_db
def test_unauthenticated_user(created_user, client) -> None:
    url = reverse("users:user-details")
    response = client.get(url, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_collect_user_reading_stats(mocker) -> None:
    # Mock the user model
    user_model = mocker.Mock()
    user = mocker.Mock()
    user_model.objects.all.return_value = [user]
    mocker.patch("users.tasks.get_user_model", return_value=user_model)

    # Create a test reading session for the 7-day period
    reading_session_7_days = mocker.Mock()
    reading_session_7_days.total_reading_time.total_seconds.return_value = (
        3600  # 1 hour
    )
    mocker.patch(
        "users.tasks.ReadingSession.objects.filter",
        return_value=[reading_session_7_days],
    )

    # Create a test reading session for the 30-day period
    reading_session_30_days = mocker.Mock()
    reading_session_30_days.total_reading_time.total_seconds.return_value = (
        7200  # 2 hours
    )
    mocker.patch(
        "users.tasks.ReadingSession.objects.filter",
        side_effect=[
            [reading_session_7_days],  # 7-day query
            [reading_session_30_days],  # 30-day query
        ],
    )

    # Set the current time to a specific date (for both 7-day and 30-day queries)
    current_time = timezone.now()
    mocker.patch("django.utils.timezone.now", return_value=current_time)

    # Execute the Celery task
    collect_user_reading_stats.apply()

    # Check that the user's attributes have been updated correctly for the 7-day period
    user.save.assert_called()
    assert user.total_reading_time_week == timedelta(seconds=3600)

    # Check that the user's attributes have been updated correctly for the 30-day period
    assert user.total_reading_time_month == timedelta(seconds=7200)
