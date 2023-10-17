from django.db.migrations import serializer
from rest_framework import generics, viewsets

from books.models import Book
from books.serializers import BookSerializer, BookListSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self) -> serializer:
        if self.action == "list":
            return BookListSerializer
        return BookSerializer
