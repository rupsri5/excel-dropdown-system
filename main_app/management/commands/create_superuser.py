# main_app/management/commands/create_superuser.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Create a superuser if none exists'

    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():
            # Get environment variables
            username = os.environ.get('SUPERUSER_USERNAME')
            email = os.environ.get('SUPERUSER_EMAIL')
            password = os.environ.get('SUPERUSER_PASSWORD')
            
            # Safety checks
            if not username or not email or not password:
                self.stdout.write(
                    self.style.ERROR(
                        'Missing environment variables: SUPERUSER_USERNAME, SUPERUSER_EMAIL, or SUPERUSER_PASSWORD'
                    )
                )
                return
            
            # Create superuser
            User.objects.create_superuser(username, email, password)
            self.stdout.write(
                self.style.SUCCESS(f'Superuser {username} created successfully')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Superuser already exists')
            )
