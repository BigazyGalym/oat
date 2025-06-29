from django.db import models
from django.conf import settings
from django.utils import timezone

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Тақырып")
    content = models.TextField(verbose_name="Мазмұны")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='news_articles',
        verbose_name="Автор"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Құрылған уақыты")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Жаңартылған уақыты")
    is_active = models.BooleanField(default=True, verbose_name="Белсенді")
    image = models.ImageField(upload_to='news_images/', null=True, blank=True, verbose_name="Сурет")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Жаңалық"
        verbose_name_plural = "Жаңалықтар"