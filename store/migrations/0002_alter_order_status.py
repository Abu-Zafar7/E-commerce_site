# Generated by Django 5.1.1 on 2024-09-09 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[("Pending", "Pending"), ("Completed", "Completed")],
                default="Pending",
                max_length=10,
            ),
        ),
    ]
