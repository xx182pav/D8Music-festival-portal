# Generated by Django 2.2.8 on 2019-12-21 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'Профиль пользователя', 'verbose_name_plural': 'Профили пользователей'},
        ),
    ]
