# Generated by Django 5.1.4 on 2024-12-25 06:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0004_alter_order_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderitem",
            name="price",
        ),
    ]