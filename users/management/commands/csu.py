from django.core.management import BaseCommand

from config.settings import get_env_values
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@sky.pro',
            first_name='Liza',
            last_name='Admin',
            is_superuser=True,
            is_staff=True,
            is_active=True
        )
        user.set_password(get_env_values('password'))
        user.save()