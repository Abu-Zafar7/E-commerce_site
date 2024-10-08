# Generated by Django 5.1.1 on 2024-09-10 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0002_alter_order_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="status",
            field=models.CharField(
                choices=[("Pending", "Pending"), ("Completed", "Completed")],
                default="Pending",
                max_length=10,
            ),
        ),
    ]
