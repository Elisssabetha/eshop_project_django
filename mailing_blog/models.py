from django.db import models

from catalog.models import NULLABLE


class MailingBlog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='mailing_blog_img/', **NULLABLE, verbose_name='Изображение')
    created_date = models.DateField(auto_now_add=True, verbose_name='Дата публикации')
    views_count = models.PositiveIntegerField(default=0, editable=False, verbose_name='Количество просмотров')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'