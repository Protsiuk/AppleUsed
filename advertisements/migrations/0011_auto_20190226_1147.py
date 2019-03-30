# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-02-26 09:47
from __future__ import unicode_literals

from django.db import migrations, models
import utils


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0010_auto_20190128_1644'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertisementimage',
            name='main_image',
        ),
        migrations.AddField(
            model_name='advertisement',
            name='main_image',
            field=models.ImageField(blank=True, default='', upload_to=utils.get_file_path, verbose_name='Main image advertisment'),
        ),
    ]