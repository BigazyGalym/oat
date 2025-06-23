from django.db import models
from django.conf import settings
from accounts.models import Profile

class ServiceType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('available', 'Доступен'),
        ('accepted', 'Принят'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершен'),
    )
    DISTRICT_CHOICES = Profile.DISTRICT_CHOICES 
    service_type = models.ForeignKey(ServiceType, on_delete=models.SET_NULL, null=True, verbose_name="Қызмет түрі")
    district = models.CharField(max_length=100, choices=DISTRICT_CHOICES, null=True, blank=True, verbose_name="Район")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name="Статус")
    customer_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_orders',
        null=True,
        verbose_name="Клиент"
    )
    worker_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='worker_orders',
        null=True,
        blank=True,
        verbose_name="Жұмысшы"
    )
    description = models.TextField(verbose_name="Сипаттама")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Құрылған уақыты")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Жаңартылган уақыты")
    rating = models.IntegerField(null=True, blank=True, verbose_name="Рейтинг")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Ұзындық")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Ені")
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Мекен-жай")
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Бағасы")
    desired_time = models.DateTimeField(null=True, blank=True, verbose_name="Қалаған уақыт")
    phone_number = models.CharField(max_length=15, null=True, blank=True, verbose_name="Телефон нөмірі")  # Жаңа өріс

    def __str__(self):
        return f"Order {self.id} - {self.status}"

    class Meta:
        verbose_name = "Тапсырыс"
        verbose_name_plural = "Тапсырыстар"