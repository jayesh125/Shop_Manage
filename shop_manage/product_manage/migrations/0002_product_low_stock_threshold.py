# Generated by Django 5.1.2 on 2024-10-16 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_manage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='low_stock_threshold',
            field=models.PositiveIntegerField(default=10),
        ),
    ]
