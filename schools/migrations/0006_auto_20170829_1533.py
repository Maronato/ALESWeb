# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-29 18:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0005_auto_20170820_0009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='facebookuser',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='custom_auth.FacebookUser'),
        ),
    ]
