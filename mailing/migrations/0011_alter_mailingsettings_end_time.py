# Generated by Django 4.2.3 on 2023-08-22 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0010_alter_mailingsettings_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailingsettings',
            name='end_time',
            field=models.DateTimeField(verbose_name='Время окончания'),
        ),
    ]