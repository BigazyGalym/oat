from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile
import logging

logger = logging.getLogger('django')

class Command(BaseCommand):
    help = 'Create missing Profile objects for users'

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            try:
                profile = user.profile
            except Profile.DoesNotExist:
                Profile.objects.create(user=user, role='customer')  # Default to 'customer'
                logger.info(f"Created profile for user {user.username}")
                self.stdout.write(self.style.SUCCESS(f'Created profile for {user.username}'))