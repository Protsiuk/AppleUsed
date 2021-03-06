# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-12-14 15:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0003_auto_20181213_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='author',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='category_equipment',
            field=models.CharField(choices=[('iMac', 'iMac'), ('MacBook', 'MacBook'), ('iPad', 'iPad'), ('Monoblok', 'Monoblok'), ('iPhone', 'iPhone'), ('iPod', 'iPod'), ('MeidaBox', 'MeidaBox'), (('Apple Watch',), 'Apple Watch')], default='iPhone', max_length=25, verbose_name='Category advertisment'),
        ),
    ]
