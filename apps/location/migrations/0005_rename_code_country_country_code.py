# Generated by Django 5.2.1 on 2025-05-22 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0004_address_map_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='country',
            old_name='code',
            new_name='country_code',
        ),
    ]
