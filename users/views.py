from django.contrib.auth import get_user_model
from django.db.models import Sum, Count
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from books.models import ReadingSession
from users.models import User
from users.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


@api_view(["GET"])
def user_stats(request) -> Response:
    """Show user's statistics"""
    user = request.user  # Get the current user

    # Calculate the total reading time for the user
    total_reading_time = ReadingSession.objects.filter(
        user=user, end_time__isnull=False
    ).aggregate(total_time=Sum("total_reading_time"))["total_time"]

    # Calculate the total number of books read by the user, considering all sessions
    total_books_read = (
        ReadingSession.objects.filter(user=user, end_time__isnull=False)
        .values("book")
        .annotate(total_sessions=Count("book"))
        .count()
    )

    # Find the current book being read (if any)
    current_session = ReadingSession.objects.filter(
        user=user, end_time__isnull=True
    ).first()

    # Find the last read book (if any)
    last_read_session = (
        ReadingSession.objects.filter(user=user, end_time__isnull=False)
        .order_by("-end_time")
        .first()
    )
    last_read_book = last_read_session.book if last_read_session else None

    stats = {
        "total_reading_time": total_reading_time.total_seconds()
        if total_reading_time
        else 0,
        "total_books_read": total_books_read,
        "current_book_being_read": current_session.book.title
        if current_session
        else None,
        "last_read_book": last_read_book.title if last_read_book else None,
        "total_reading_time_7_days": user.total_reading_time_week,
        "total_reading_time_30_days": user.total_reading_time_month,
    }

    return Response(stats, status=status.HTTP_200_OK)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Show information about current user"""

    serializer_class = UserSerializer

    def get_object(self) -> User:
        return get_user_model().objects.get(id=self.request.user.id)
