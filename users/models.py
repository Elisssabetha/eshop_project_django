from django.contrib.auth.models import AbstractUser
from django.db import models

from catalog.models import NULLABLE


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')

    avatar = models.ImageField(upload_to='users/', **NULLABLE, verbose_name='Аватар')
    phone = models.CharField(max_length=35, verbose_name='Номер телефона')
    country = models.CharField(max_length=150, verbose_name='Страна')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        # кастомное право доступа на блокировку пользователя
        permissions = [
            ('set_is_active', 'Can change is_active')
        ]