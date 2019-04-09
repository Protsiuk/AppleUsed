# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-04-09 10:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0015_auto_20190314_1133'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='advertisement',
            options={'verbose_name': 'Advertisement', 'verbose_name_plural': 'Advertisements'},
        ),
        migrations.AddField(
            model_name='advertisement',
            name='is_visible',
            field=models.BooleanField(default=False),
        ),
    ]