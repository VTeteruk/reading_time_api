from django.db.models import Sum
from rest_framework import serializers
from books.models import Book, ReadingSession


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
    user_total_reading_time = serializers.SerializerMethodField()

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
            "user_total_reading_time",
        )
        read_only_fields = ("id", "last_time_read")

    def to_representation(self, instance) -> dict:
        data = super().to_representation(instance)
        data.pop("short_description")
        return data

    def get_user_total_reading_time(self, instance) -> int | float:
        user = self.context["request"].user
        total_reading_time = ReadingSession.objects.filter(
            user=user, book=instance, end_time__isnull=False
        ).aggregate(total_time=Sum("total_reading_time"))["total_time"]
        return total_reading_time.total_seconds() if total_reading_time else 0

    def create(self, validated_data) -> Book:
        """If full_description is not provided, use short_description"""
        if not validated_data.get("full_description"):
            validated_data["full_description"] = validated_data[
                "short_description"
            ]
        return Book.objects.create(**validated_data)


class BookReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = set()
