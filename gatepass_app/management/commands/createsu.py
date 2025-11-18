from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = "Creates the default superuser from environment variables if not exists."

    def handle(self, *args, **options):

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
        first_name = os.environ.get("DJANGO_SUPERUSER_FIRSTNAME", "")
        last_name = os.environ.get("DJANGO_SUPERUSER_LASTNAME", "")

        # If any essential values missing → skip
        if not username or not password:
            self.stdout.write("Superuser environment variables not set. Skipping.")
            return

        # If superuser already exists → skip
        if User.objects.filter(username=username).exists():
            self.stdout.write(f"Superuser '{username}' already exists. Skipping.")
            return

        # Create superuser
        self.stdout.write(f"Creating superuser '{username}'...")
        user = User.objects.create_superuser(
            username=username,
            password=password,
            email=email
        )

        user.first_name = first_name
        user.last_name = last_name
        user.save()

        self.stdout.write("Superuser created successfully!")
