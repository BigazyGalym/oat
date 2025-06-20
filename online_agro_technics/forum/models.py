from django.db import models
from django.conf import settings
from django.utils import timezone

class ForumPost(models.Model):
    title = models.CharField(max_length=200, verbose_name="Тақырып")
    content = models.TextField(verbose_name="Мазмұны")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='forum_posts',
        verbose_name="Автор"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Құрылған уақыты")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Жаңартылған уақыты")
    is_active = models.BooleanField(default=True, verbose_name="Белсенді")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Форум жазбасы"
        verbose_name_plural = "Форум жазбалары"

class ForumComment(models.Model):
    post = models.ForeignKey(
        ForumPost,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Жазба"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='forum_comments',
        verbose_name="Автор"
    )
    content = models.TextField(verbose_name="Пікір мазмұны")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Құрылған уақыты")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Жаңартылған уақыты")

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

    class Meta:
        verbose_name = "Форум пікірі"
        verbose_name_plural = "Форум пікірлері"