from django.core.management.base import BaseCommand
from myapp.models import User  # Import your custom User model

class Command(BaseCommand):
    help = 'Populates the database with user data'

    def handle(self, *args, **kwargs):
        password = 'Ihavefive$'
        users_data = [
            {"name": "Alice", "username": "alice", "email": "alice@example.com"},
            {"name": "Bob", "username": "bob", "email": "bob@example.com"},
            {"name": "Charlie", "username": "charlie", "email": "charlie@example.com"},
            {"name": "David", "username": "david", "email": "david@example.com"},
            {"name": "Eve", "username": "eve", "email": "eve@example.com"},
            # Add more users as needed
        ]

        for user_data in users_data:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=password,
                )
                user.name = user_data['name']  # Assuming 'name' is a field in your custom User model
                user.save()
                self.stdout.write(self.style.SUCCESS(f"User {user_data['username']} created"))
            else:
                self.stdout.write(self.style.WARNING(f"User {user_data['username']} already exists"))
