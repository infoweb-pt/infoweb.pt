import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create an initial superuser from DB_USER and DB_PASSWORD when none exists.'

    def handle(self, *args, **options):
        User = get_user_model()

        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write('Superuser already exists; skipping.')
            return

        username = os.environ.get('DB_USER') or 'infoweb'
        password = os.environ.get('DB_PASSWORD') or 'changeme'
        email = os.environ.get('SUPERUSER_EMAIL') or ''

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Created superuser "{username}".'))
