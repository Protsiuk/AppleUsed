# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-04-13 06:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0017_auto_20190409_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='category_equipment',
            field=models.CharField(choices=[('iMac', 'iMac'), ('MacBook', 'MacBook'), ('iPad', 'iPad'), ('Monoblok', 'Monoblok'), ('iPhone', 'iPhone'), ('iPod', 'iPod'), ('MeidaBox', 'MeidaBox'), ('Apple Watch', 'Apple Watch'), ('Accessory', 'Accessory')], default='iPhone', max_length=25, verbose_name='Category advertisement'),
        ),
    ]
