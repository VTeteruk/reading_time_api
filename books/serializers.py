from rest_framework import serializers
from books.models import Book


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "publication_year",
            "short_description",
        )


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "publication_year",
            "short_description",
            "full_description",
            "last_time_read",
        )
        read_only_fields = ("id", "last_time_read")

    def to_representation(self, instance) -> dict:
        return {
            "id": instance.id,
            "title": instance.title,
            "author": instance.author,
            "publication_year": instance.publication_year,
            "full_description": instance.full_description,
            "last_time_read": instance.last_time_read
        }

    def create(self, validated_data) -> Book:
        """If full_description is not provided, use short_description"""
        if not validated_data.get("full_description"):
            validated_data["full_description"] = validated_data["short_description"]
        return Book.objects.create(**validated_data)
