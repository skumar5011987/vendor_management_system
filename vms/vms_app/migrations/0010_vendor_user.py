# Generated by Django 4.2.8 on 2023-12-09 13:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vms_app', '0009_alter_historicalperformance_vendor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
