from os.path import join

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book, ReadingSession


@pytest.fixture()
def get_book_path() -> str:
    return "/api/books/"


@pytest.fixture()
def sample_book_data() -> dict:
    return {
        "title": "Test Book",
        "author": "Test Author",
        "publication_year": 2022,
    }


@pytest.fixture()
def authenticated_user() -> APIClient:
    user = get_user_model().objects.create_user(
        username="testuser",
        first_name="test",
        last_name="test",
        password="testpassword",
    )
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture()
def create_book(sample_book_data) -> Book:
    return Book.objects.create(**sample_book_data)


@pytest.mark.django_db
def test_unauthenticated_book(client, sample_book_data, get_book_path) -> None:
    response = client.get(get_book_path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.post(get_book_path, sample_book_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.post(join(get_book_path, "1/"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.post(join(get_book_path, "1/read/"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_book_viewset_list(
    authenticated_user, get_book_path, create_book
) -> None:
    # Test the list view
    response = authenticated_user.get(get_book_path)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data.get("count") == 1


@pytest.mark.django_db
def test_book_viewset_read(
    authenticated_user, get_book_path, create_book
) -> None:
    # Test the read action to start a session
    response = authenticated_user.post(
        join(get_book_path, f"{create_book.id}/read/")
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Reading session started for the book"

    # Test the read action again to end the session
    response = authenticated_user.post(
        join(get_book_path, f"{create_book.id}/read/")
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Reading session ended for the book"

    assert ReadingSession.objects.count() == 1
    assert ReadingSession.objects.get(id=1).start_time is not None
    assert ReadingSession.objects.get(id=1).end_time is not None

    response = authenticated_user.get(
        join(get_book_path, f"{create_book.id}/")
    )
    assert response.json()["last_time_read"] is not None
