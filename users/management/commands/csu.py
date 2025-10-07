import os

from django.core.management import BaseCommand
from dotenv import load_dotenv

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        load_dotenv()

        user = User.objects.create(email=os.getenv("ADMIN_MAIL"))
        user.set_password(os.getenv("ADMIN_PASS"))
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
