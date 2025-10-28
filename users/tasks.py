from celery import shared_task
from datetime import timedelta
from django.utils import timezone

from users.models import User

@shared_task
def deactivate_inactive_users():
    cutoff = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(is_active=True, last_login__lt=cutoff)

    never_logged_in_users = User.objects.filter(is_active=True, last_login__isnull=True)

    all_inactive_users = inactive_users.union(never_logged_in_users)

    all_inactive_users.update(is_active=False)
    return all_inactive_users