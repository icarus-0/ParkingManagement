# Generated by Django 4.1.3 on 2022-12-07 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_remove_vehicleparking_status_parkingspace_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkingspace',
            name='vehicle_parked',
            field=models.CharField(max_length=50, null=True),
        ),
    ]