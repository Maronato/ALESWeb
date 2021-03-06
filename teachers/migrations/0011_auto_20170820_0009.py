# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-20 03:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0003_auto_20170703_2114'),
        ('teachers', '0010_auto_20170406_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='facebook_create_url',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='teacher',
            name='facebookuser',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='custom_auth.FacebookUser'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='has_facebook',
            field=models.BooleanField(default=False),
        ),
    ]
