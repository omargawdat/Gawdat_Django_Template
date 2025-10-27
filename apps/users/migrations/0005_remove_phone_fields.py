# Generated manually to remove phone_number and phone_verified fields

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_user_phone_verified_alter_user_email"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="phone_number",
        ),
        migrations.RemoveField(
            model_name="user",
            name="phone_verified",
        ),
    ]
