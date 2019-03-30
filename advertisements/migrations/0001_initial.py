# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-12-11 16:02
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title advertisment')),
                ('category_equipment', models.CharField(choices=[('iMac', 'iMac'), ('MacBook', 'MacBook'), ('iPad', 'iPad'), ('Monoblok', 'Monoblok'), ('iPhone', 'iPhone'), ('iPod', 'iPod'), ('iPod', 'iPod'), (('Apple Watch',), 'Apple Watch')], default='iPhone', max_length=25, verbose_name='Category advertisment')),
                ('phone_author', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+9999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Phone number author')),
                ('description', models.TextField(verbose_name='Description advertisment')),
                ('price', models.CharField(max_length=255, verbose_name='Price advertisment')),
                ('product_number', models.CharField(blank=True, default='', max_length=25, verbose_name='Manufacture/serial number')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Advertisments',
                'verbose_name': 'Advertisment',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='AdvertisementFollowing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisements.Advertisement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AdvertisementImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default='', upload_to=utils.get_file_path, verbose_name='Image advertisment')),
                ('main_image', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('advertisment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisements.Advertisement')),
            ],
        ),
        migrations.CreateModel(
            name='AdvertisementMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_visitor', models.EmailField(max_length=50, verbose_name='Email')),
                ('text', models.TextField(max_length=500, verbose_name='Text message')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('advertisement', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='advertisements.Advertisement')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default='Site name', max_length=255)),
                ('maintenance_mode', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Site Configuration',
            },
        ),
    ]