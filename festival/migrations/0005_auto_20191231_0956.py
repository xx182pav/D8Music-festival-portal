# Generated by Django 2.2.8 on 2019-12-31 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('festival', '0004_auto_20191231_0947'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='scene',
        ),
        migrations.AddField(
            model_name='request',
            name='desired_scene',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='festival.Scene', verbose_name='Желаемая сцена'),
        ),
        migrations.AddField(
            model_name='request',
            name='desired_timeslot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='festival.TimeSlot', verbose_name='Желаемое время выступления'),
        ),
    ]
