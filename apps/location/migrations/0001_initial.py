# Generated by Django 5.2.1 on 2025-05-25 11:10

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('restored_at', models.DateTimeField(blank=True, null=True)),
                ('transaction_id', models.UUIDField(blank=True, null=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='Location Point')),
                ('description', models.TextField(verbose_name='Description')),
                ('map_description', models.TextField(default='', help_text='Description for the map view', verbose_name='Map Description')),
                ('location_type', models.CharField(choices=[('HOME', 'Home'), ('WORK', 'Work')], max_length=10, verbose_name='Location Type')),
                ('map_image', models.ImageField(blank=True, help_text='Image of the location on the map', null=True, upload_to='location/map_images/', verbose_name='Map Image')),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('code', models.CharField(choices=[('EG', 'Egypt'), ('SA', 'Saudi Arabia'), ('AE', 'United Arab Emirates'), ('KW', 'Kuwait'), ('QA', 'Qatar'), ('OM', 'Oman'), ('BH', 'Bahrain')], max_length=3, primary_key=True, serialize=False, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('name_ar', models.CharField(max_length=100, null=True, unique=True, verbose_name='Name')),
                ('name_en', models.CharField(max_length=100, null=True, unique=True, verbose_name='Name')),
                ('currency', models.CharField(choices=[('EGP', 'Egyptian Pound'), ('SAR', 'Saudi Riyal'), ('AED', 'Emirati Dirham'), ('KWD', 'Kuwaiti Dinar'), ('QAR', 'Qatari Riyal'), ('OMR', 'Omani Rial'), ('BHD', 'Bahraini Dinar')], max_length=3, verbose_name='Currency')),
                ('flag', models.ImageField(upload_to='flags', verbose_name='Flag')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('phone_code', models.CharField(max_length=4, verbose_name='Number Code')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('code', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('name_ar', models.CharField(max_length=255, null=True, verbose_name='Name')),
                ('name_en', models.CharField(max_length=255, null=True, verbose_name='Name')),
                ('geometry', django.contrib.gis.db.models.fields.GeometryField(srid=4326, verbose_name='Geometry')),
            ],
            options={
                'verbose_name': 'Region',
                'verbose_name_plural': 'Regions',
            },
        ),
    ]
