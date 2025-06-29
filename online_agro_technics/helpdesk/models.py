from django.db import models
from django.conf import settings
from orders.models import ServiceType
from django.utils import timezone

class Ticket(models.Model):
    STATUS_CHOICES = (
        ('new', 'Жаңа'),
        ('in_progress', 'Өңделуде'),
        ('closed', 'Жабылған'),
    )
    PRIORITY_CHOICES = (
        ('low', 'Төмен'),
        ('medium', 'Орташа'),
        ('high', 'Жоғары'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets',
        verbose_name="Клиент"
    )
    service_type = models.ForeignKey(
        ServiceType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Қызмет түрі"
    )
    title = models.CharField(max_length=200, verbose_name="Тақырып")
    description = models.TextField(verbose_name="Сипаттама")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name="Басымдық")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Құрылған уақыт")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Жаңартылған уақыт")
    file = models.FileField(upload_to='tickets/', null=True, blank=True, verbose_name="Файл")

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Тікет"
        verbose_name_plural = "Тікеттер"

class TicketResponse(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name="Тікет"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ticket_responses',
        verbose_name="Автор"
    )
    message = models.TextField(verbose_name="Хабарлама")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Құрылған уақыт")
    file = models.FileField(upload_to='ticket_responses/', null=True, blank=True, verbose_name="Файл")

    def __str__(self):
        return f"Response by {self.user.username} on {self.ticket.title}"

    class Meta:
        verbose_name = "Тікет жауабы"
        verbose_name_plural = "Тікет жауаптары"

class HelpdeskTicket(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('in_progress', 'В процессе'),
        ('resolved', 'Решено'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title