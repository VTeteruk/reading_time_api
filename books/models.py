from django.contrib.auth import get_user_model
from django.db import models


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


class ReadingSession(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name="users", on_delete=models.CASCADE
    )
    book = models.ForeignKey(
        Book, related_name="sessions", on_delete=models.CASCADE
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    total_reading_time = models.DurationField(null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username + " reads " + self.book.title
