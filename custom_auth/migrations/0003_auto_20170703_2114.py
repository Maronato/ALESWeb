# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-04 00:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0002_auto_20170703_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facebookuser',
            name='thumbnail_age',
            field=models.DateTimeField(null=True),
        ),
    ]
