# Generated by Django 4.2.8 on 2023-12-09 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vms_app', '0007_alter_purchaseorder_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalperformance',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vender_history', to='vms_app.vendor'),
        ),
    ]
