# Generated by Django 4.2.3 on 2023-07-18 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_blog_preview'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='preview',
            new_name='image',
        ),
    ]
