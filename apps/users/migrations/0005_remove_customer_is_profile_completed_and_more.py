# Generated by Django 5.1.7 on 2025-04-22 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customer_is_profile_completed_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='is_profile_completed',
        ),
        migrations.RemoveField(
            model_name='historicalcustomer',
            name='is_profile_completed',
        ),
    ]
