# Generated by Django 4.2.8 on 2023-12-07 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vms_app', '0002_alter_historicalperformance_average_response_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='vendor_code',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
    ]
