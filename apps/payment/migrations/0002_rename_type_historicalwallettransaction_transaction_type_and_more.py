# Generated by Django 5.1.7 on 2025-04-22 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalwallettransaction',
            old_name='type',
            new_name='transaction_type',
        ),
        migrations.RenameField(
            model_name='wallettransaction',
            old_name='type',
            new_name='transaction_type',
        ),
    ]
