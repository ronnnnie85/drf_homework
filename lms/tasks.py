from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

from lms.models import Course, Subscription

@shared_task
def send_course_update_emails(course_id: int):
    course = Course.objects.filter(id=course_id).first()
    if not course:
        return

    subs = Subscription.objects.filter(course=course).select_related("user")
    if not subs.exists():
        return

    subject = f"Обновление материалов курса «{course.name}»"
    message = (
        f"Материалы курса «{course.name}» были обновлены.\n\n"
        f"Описание: {course.description or '—'}\n"
    )
    from_email = getattr(settings, "EMAIL_HOST_USER")

    for sub in subs:
        recipient = getattr(sub.user, "email")
        if not recipient:
            continue
        try:
            send_mail(subject, message, from_email, [recipient], fail_silently=True)
        except Exception:
            pass