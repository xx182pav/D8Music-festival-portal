# Generated by Django 2.2.8 on 2019-12-30 23:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('festival', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sceneslot',
            name='request',
        ),
    ]
