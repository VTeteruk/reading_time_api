import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_year = models.PositiveIntegerField()
    short_description = models.TextField()
    full_description = models.TextField(null=True, blank=True)
    last_time_read = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("title", "author", "publication_year")

    def save(self, *args, **kwargs) -> None:
        """If full_description is not provided, use short_description"""
        if not self.full_description:
            self.full_description = self.short_description
        super(Book, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    @property
    def total_reading_time(self) -> datetime:
        """Calculate the total reading time for this book by summing the durations
        of all related ReadingSession objects"""
        total_time = self.sessions.filter(total_reading_time__isnull=False).aggregate(
            total_time=Sum("total_reading_time")
        )["total_time"]

        # If there is no total time, return a default value of 0
        return total_time or datetime.timedelta(0)


class ReadingSession(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name="users", on_delete=models.CASCADE
    )
    book = models.ForeignKey(Book, related_name="sessions", on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    total_reading_time = models.DurationField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user.name} reads {self.book.title}"
