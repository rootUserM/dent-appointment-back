# Generated by Django 4.2.6 on 2024-02-12 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0012_service_appointment_status_alter_createregisbase_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createregisbase',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
