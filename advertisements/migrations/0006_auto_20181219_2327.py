# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-12-19 21:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0005_auto_20181214_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisementimage',
            name='advertisement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='advertisements.Advertisement'),
        ),
    ]
