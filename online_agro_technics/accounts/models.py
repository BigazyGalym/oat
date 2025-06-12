from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_active = False
        super().save(*args, **kwargs)

class Profile(models.Model):
    ROLE_CHOICES = (
        ('customer', 'Заказчик'),
        ('worker', 'Рабочий'),
        ('admin', 'Админ'),
    )
    DISTRICT_CHOICES = (
        ('almalinsky', 'Алмалинский район'),
        ('alatau', 'Алатауский район'),
        ('auezov', 'Ауэзовский район'),
        ('bostandyk', 'Бостандыкский район'),
        ('zhetysu', 'Жетысуский район'),
        ('medeu', 'Медеуский район'),
        ('nauryzbay', 'Наурызбайский район'),
        ('turksib', 'Турксибский район'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True)
    description = models.TextField(blank=True)
    is_worker = models.BooleanField(default=False)
    completed_orders = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    district = models.CharField(max_length=100, choices=DISTRICT_CHOICES, null=True, blank=True, help_text="Рабочийдің қызмет көрсету ауданы")
    phone_number = models.CharField(max_length=15, blank=False, null=False)
    service_type = models.ForeignKey('orders.ServiceType', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    def is_admin(self):
        return self.role == 'admin'

class EmailVerificationCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Verification for {self.user.username} - {self.code}"

    def is_expired(self):
        return timezone.now() > self.expires_at