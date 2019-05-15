# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-05-14 15:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20190506_1447'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='temporary_user',
            new_name='temporary_user_email',
        ),
        migrations.AddField(
            model_name='message',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Was read'),
        ),
        migrations.AlterField(
            model_name='message',
            name='subject_ad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisements.Advertisement', verbose_name='Dialog about'),
        ),
    ]
