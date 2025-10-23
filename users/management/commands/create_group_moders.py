import os

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from dotenv import load_dotenv


class Command(BaseCommand):
    help = "Создаёт группу с именем из переменной окружения MOD_GROUP (без назначения прав)."

    def handle(self, *args, **options):
        load_dotenv()
        group_name = os.getenv("MOD_GROUP")
        if not group_name:
            self.stderr.write(
                self.style.ERROR("Переменная окружения MOD_GROUP не установлена.")
            )
            return 1

        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            self.stdout.write(self.style.SUCCESS(f"Группа '{group_name}' создана."))
        else:
            self.stdout.write(
                self.style.WARNING(f"Группа '{group_name}' уже существует.")
            )
        return 0
