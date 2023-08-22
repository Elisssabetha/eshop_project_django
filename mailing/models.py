from django.conf import settings
from django.db import models

from catalog.models import NULLABLE


class Customer(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=150, **NULLABLE, verbose_name='Имя')
    last_name = models.CharField(max_length=150, **NULLABLE, verbose_name='Фамилия')
    comment = models.TextField(**NULLABLE, verbose_name='Комментарий')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    subject = models.CharField(max_length=250, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                              verbose_name='Пользователь')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class MailingSettings(models.Model):
    PERIOD_DAILY = 'daily'
    PERIOD_WEEKLY = 'weekly'
    PERIOD_MONTHLY = 'monthly'

    PERIODS = (
        (PERIOD_DAILY, 'Ежедневная'),
        (PERIOD_WEEKLY, 'Раз в неделю'),
        (PERIOD_MONTHLY, 'Раз в месяц')

    )

    STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'
    STATUS_DONE = 'done'

    STATUSES = (
        (STATUS_STARTED, 'Запущена'),
        (STATUS_CREATED, 'Создана'),
        (STATUS_DONE, 'Завершена')
    )

    start_time = models.DateTimeField(verbose_name='Время старта')
    end_time = models.DateTimeField(verbose_name='Время окончания')
    period = models.CharField(max_length=20, choices=PERIODS, verbose_name='Периодичность')
    status = models.CharField(max_length=20, choices=STATUSES, verbose_name='Статус рассылки')

    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                              verbose_name='Пользователь')
    def __str__(self):
        return f"{self.start_time} - {self.period}"

    class Meta:
        verbose_name = 'Paccылка'
        verbose_name_plural = 'Рассылки'
        ordering = ('start_time',)

        # кастомное право доступа на отключение рассылок
        permissions = [
            ('set_status', 'Can change status')
        ]


class MailingClient(models.Model):
    client = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Клиент')
    settings = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='Настройки')

    def __str__(self):
        return f'{self.client} - {self.settings}'

    class Meta:
        verbose_name = 'Клиент рассылки'
        verbose_name_plural = 'Клиенты рассылки'


class MailingLog(models.Model):
    STATUS_OK = 'ok'
    STATUS_FAILED = 'failed'
    STATUSES = (
        (STATUS_OK, 'Успешно'),
        (STATUS_FAILED, 'Ошибка')
    )

    last_try = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки')
    client = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Клиент')
    settings = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='Настройки')
    status = models.CharField(max_length=20, choices=STATUSES, default=STATUS_OK, verbose_name='Статус')
    server_response = models.TextField(**NULLABLE, verbose_name='Ответ сервера')

    def __str__(self):
        return f"{self.last_try}"

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
