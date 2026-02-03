# core/management/commands/create_admin.py

import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Superuser yaratadi (.env dan)'

    def handle(self, *args, **options):
        username = "muhammadali_bovaqulov"
        email = "bovaqulov@gmail.com"
        password = "asadbek0808$1"

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'✅ Superuser "{username}" yaratildi!')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Superuser "{username}" allaqachon mavjud!')
            )