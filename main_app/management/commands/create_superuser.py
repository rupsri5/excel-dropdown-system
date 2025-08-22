# main_app/management/commands/create_superuser.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Create a superuser if none exists'

    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():
            username = os.environ.get('SUPERUSER_USERNAME')
            email = os.environ.get('SUPERUSER_EMAIL')
            password = os.environ.get('SUPERUSER_PASSWORD')
            
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'Superuser {username} created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))
