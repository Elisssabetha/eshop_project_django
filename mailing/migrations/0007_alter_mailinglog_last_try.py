# Generated by Django 4.2.3 on 2023-08-19 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0006_mailinglog_last_try'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailinglog',
            name='last_try',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки'),
        ),
    ]
