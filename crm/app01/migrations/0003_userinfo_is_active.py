# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-12-05 08:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20191205_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
