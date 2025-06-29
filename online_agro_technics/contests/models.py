from django.db import models
from django.conf import settings
from django.utils import timezone

class Contest(models.Model):
    title = models.CharField(max_length=200, verbose_name="Тақырып")
    description = models.TextField(verbose_name="Сипаттама")
    start_date = models.DateTimeField(verbose_name="Басталу уақыты")
    end_date = models.DateTimeField(verbose_name="Аяқталу уақыты")
    prize = models.CharField(max_length=200, verbose_name="Сыйлық")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Құрылған уақыты")
    is_active = models.BooleanField(default=True, verbose_name="Белсенді")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Конкурс"
        verbose_name_plural = "Конкурстар"

class ContestEntry(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='entries', verbose_name="Конкурс")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contest_entries', verbose_name="Қатысушы")
    submission = models.TextField(verbose_name="Жұмыс")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Жіберілген уақыты")

    def __str__(self):
        return f"{self.user.username} - {self.contest.title}"

    class Meta:
        verbose_name = "Конкурсқа қатысу"
        verbose_name_plural = "Конкурсқа қатысулар"