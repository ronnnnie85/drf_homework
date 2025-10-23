from datetime import date

from django.core.management.base import BaseCommand

from lms.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    help = "Создаёт тестовые записи в таблице Payment и удаляет старые записи"

    def handle(self, *args, **kwargs):
        deleted_count, _ = Payment.objects.all().delete()
        self.stdout.write(
            self.style.WARNING(f"🗑 Удалено старых записей: {deleted_count}")
        )

        user = User.objects.first()

        lessons = Lesson.objects.all()[:2]
        course = Course.objects.first()

        if not user:
            self.stdout.write(self.style.ERROR("Нет пользователей в базе"))
            return

        if lessons.count() < 2:
            self.stdout.write(self.style.ERROR("Нужно минимум 2 урока в базе"))
            return

        if not course:
            self.stdout.write(self.style.ERROR("Нет курсов в базе"))
            return

        payments = [
            Payment(
                user=user,
                payment_date=date(2025, 10, 1),
                amount=1500,
                payment_method="cash",
                paid_lesson=lessons[0],
            ),
            Payment(
                user=user,
                payment_date=date(2025, 10, 3),
                amount=2000,
                payment_method="transfer",
                paid_lesson=lessons[1],
            ),
            Payment(
                user=user,
                payment_date=date(2025, 10, 5),
                amount=5000,
                payment_method="transfer",
                paid_course=course,
            ),
        ]

        Payment.objects.bulk_create(payments)
        self.stdout.write(
            self.style.SUCCESS("Успешно добавлено 3 записи в таблицу Payment")
        )
