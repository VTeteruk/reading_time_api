from django.contrib import admin

from books.models import Book, ReadingSession

admin.site.register(Book)
admin.site.register(ReadingSession)
