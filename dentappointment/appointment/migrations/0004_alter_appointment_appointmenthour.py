# Generated by Django 4.2.6 on 2023-10-23 02:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0003_alter_appointment_appointmenthour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='appointmentHour',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]