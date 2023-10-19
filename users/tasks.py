import logging

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from books.models import ReadingSession

logger = logging.getLogger(__name__)


@shared_task
def collect_user_reading_stats() -> None:
    users = get_user_model().objects.all()

    for user in users:
        try:
            logger.info("Celery task started")
            seven_days_ago = timezone.now() - timedelta(days=7)
            thirty_days_ago = timezone.now() - timedelta(days=30)

            total_reading_time_week_sessions = ReadingSession.objects.filter(
                user=user, start_time__gte=seven_days_ago, end_time__isnull=False
            )

            total_reading_time_month_sessions = ReadingSession.objects.filter(
                user=user, start_time__gte=thirty_days_ago, end_time__isnull=False
            )

            total_reading_time_week_seconds = sum(
                (
                    session.total_reading_time.total_seconds()
                    for session in total_reading_time_week_sessions
                ),
                0,
            )

            total_reading_time_month_seconds = sum(
                (
                    session.total_reading_time.total_seconds()
                    for session in total_reading_time_month_sessions
                ),
                0,
            )

            total_reading_time_week_timedelta = timedelta(
                seconds=total_reading_time_week_seconds
            )
            total_reading_time_month_timedelta = timedelta(
                seconds=total_reading_time_month_seconds
            )

            user.total_reading_time_week = total_reading_time_week_timedelta
            user.total_reading_time_month = total_reading_time_month_timedelta
            user.save()
            logger.info("Celery task completed")
        except Exception as e:
            logger.error(f"Celery task error: {e}")
