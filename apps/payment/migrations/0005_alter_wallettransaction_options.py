# Generated by Django 5.1.7 on 2025-04-22 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_alter_wallettransaction_wallet'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wallettransaction',
            options={'ordering': ['-created_at'], 'verbose_name': 'Wallet Transaction', 'verbose_name_plural': 'Wallet Transactions'},
        ),
    ]
