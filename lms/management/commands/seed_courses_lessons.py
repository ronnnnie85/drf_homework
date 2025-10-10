from django.core.management.base import BaseCommand
from django.db import transaction

from lms.models import Course, Lesson


class Command(BaseCommand):
    help = "Очищает таблицы Course/Lesson и заполняет 2 курсами (Математика, Физика) и 4 уроками (по 2 на курс)."

    @transaction.atomic
    def handle(self, *args, **options):

        deleted_lessons, _ = Lesson.objects.all().delete()
        deleted_courses, _ = Course.objects.all().delete()
        self.stdout.write(
            self.style.WARNING(
                f"Удалено: уроков={deleted_lessons}, курсов={deleted_courses}"
            )
        )

        math = Course.objects.create(
            name="Математика", description="Базовый курс по математике"
        )
        physics = Course.objects.create(
            name="Физика", description="Базовый курс по физике"
        )

        lessons = [
            Lesson(
                course=math,
                name="Математика — Урок 1",
                description="Введение в математику",
                video="https://example.com/math-lesson-1",
            ),
            Lesson(
                course=math,
                name="Математика — Урок 2",
                description="Алгебра: основы",
                video="https://example.com/math-lesson-2",
            ),
            Lesson(
                course=physics,
                name="Физика — Урок 1",
                description="Введение в физику",
                video="https://example.com/physics-lesson-1",
            ),
            Lesson(
                course=physics,
                name="Физика — Урок 2",
                description="Механика: основы",
                video="https://example.com/physics-lesson-2",
            ),
        ]
        Lesson.objects.bulk_create(lessons)

        self.stdout.write(self.style.SUCCESS("Создано: курсов=2 , уроков=4"))
