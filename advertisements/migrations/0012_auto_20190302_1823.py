# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-03-02 16:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0011_auto_20190226_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisementfollowing',
            name='advertisement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='advertisements.Advertisement'),
        ),
        migrations.AlterField(
            model_name='advertisementfollowing',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
    ]
