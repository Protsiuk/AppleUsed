# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-04-20 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0018_auto_20190413_0922'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='is_moderated',
            field=models.BooleanField(default=False),
        ),
    ]
