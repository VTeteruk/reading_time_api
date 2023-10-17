from django.db.models import Sum, Count
from django.utils import timezone

from django.db.migrations import serializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from books.models import Book, ReadingSession
from books.serializers import BookSerializer, BookListSerializer, BookReadSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self) -> serializer:
        if self.action == "list":
            return BookListSerializer
        if self.action == "read":
            return BookReadSerializer
        return BookSerializer

    @action(detail=True, methods=["POST"], url_path="read")
    def read(self, request, pk=None) -> Response:
        book = self.get_object()  # Get the book instance
        user = request.user  # Assuming you have a user profile

        # Check if the user has an ongoing reading session for the same book
        current_session = ReadingSession.objects.filter(
            user=user, book=book, end_time__isnull=True
        ).first()

        if current_session:
            # If there is an ongoing session for the same book, end it
            current_session.end_time = timezone.now()

            current_session.total_reading_time = (
                current_session.end_time - current_session.start_time
            )
            current_session.save()
            # Set last_time_read to the end time of the session
            book.last_time_read = current_session.end_time
            book.save()
            return Response(
                {"message": "Reading session ended for the book"},
                status=status.HTTP_200_OK,
            )

        # Check if the user has an ongoing reading session for a different book
        current_session = ReadingSession.objects.filter(
            user=user, end_time__isnull=True
        ).first()

        # If there is an ongoing session for a different book, end it
        if current_session:
            current_session.end_time = timezone.now()
            current_session.save()

        # Create a new reading session for the current book
        ReadingSession.objects.create(user=user, book=book, start_time=timezone.now())
        # Set last_time_read to None when starting a new session
        book.last_time_read = None
        book.save()

        return Response(
            {"message": "Reading session started for the book"},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["GET"], url_path="user-stats")
    def user_stats(self, request) -> Response:
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

        user_stats = {
            "total_reading_time": total_reading_time.total_seconds()
            if total_reading_time
            else 0,
            "total_books_read": total_books_read,
            "current_book_being_read": current_session.book.title
            if current_session
            else None,
            "last_read_book": last_read_book.title if last_read_book else None,
        }

        return Response(user_stats, status=status.HTTP_200_OK)
