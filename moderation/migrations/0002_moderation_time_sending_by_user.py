# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-04-09 11:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='moderation',
            name='time_sending_by_user',
            field=models.DateTimeField(auto_now=True, verbose_name='Time sending ad by user for checking'),
        ),
    ]