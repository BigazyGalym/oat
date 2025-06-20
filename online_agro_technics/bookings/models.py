from django.db import models
from django.conf import settings
from orders.models import ServiceType
from accounts.models import Profile

class WorkerAvailability(models.Model):
    worker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='availabilities',
        verbose_name="Жұмысшы"
    )
    service_type = models.ForeignKey(
        ServiceType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Қызмет түрі"
    )
    start_time = models.DateTimeField(verbose_name="Басталу уақыты")
    end_time = models.DateTimeField(verbose_name="Аяқталу уақыты")
    is_available = models.BooleanField(default=True, verbose_name="Бос па")

    def __str__(self):
        return f"{self.worker.username} - {self.start_time} to {self.end_time}"

    class Meta:
        verbose_name = "Жұмысшының бос уақыты"
        verbose_name_plural = "Жұмысшылардың бос уақыттары"

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Күтуде'),
        ('confirmed', 'Растаулы'),
        ('cancelled', 'Жойылған'),
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name="Клиент"
    )
    worker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='worker_bookings',
        verbose_name="Жұмысшы"
    )
    availability = models.ForeignKey(
        WorkerAvailability,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name="Бос уақыт"
    )
    service_type = models.ForeignKey(
        ServiceType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Қызмет түрі"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Құрылған уақыты")
    notes = models.TextField(blank=True, verbose_name="Ескертпелер")

    def __str__(self):
        return f"Booking {self.id} by {self.customer.username} with {self.worker.username}"

    class Meta:
        verbose_name = "Бронь"
        verbose_name_plural = "Броньдар"