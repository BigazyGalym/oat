from django.db import models
from django.conf import settings

class SubsidyInquiry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subsidy_inquiries', verbose_name="Клиент")
    message = models.TextField(verbose_name="Сұрау")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Құрылған уақыты")
    responded = models.BooleanField(default=False, verbose_name="Жауап берілді")

    def __str__(self):
        return f"Inquiry by {self.user.username}"

    class Meta:
        verbose_name = "Субсидия сұрауы"
        verbose_name_plural = "Субсидия сұраулары"