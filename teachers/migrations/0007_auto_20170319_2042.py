# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-19 23:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0006_auto_20170319_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emaillist',
            name='greeting',
            field=models.CharField(choices=[('Love', 'Love'), ('Atenciosamente', 'Atenciosamente'), ('Cordialmente', 'Cordialmente'), ('Saudações', 'Saudações'), ('Regards', 'Regards'), ('Yours truly', 'Yours truly'), ('Sincerely', 'Sincerely'), ('Abraço', 'Abraço'), ('Obrigado', 'Obrigado'), ('Obrigada', 'Obrigada'), ('Obrigadx', 'Obrigadx'), ('Beijos', 'Beijos'), ('XOXO', 'XOXO'), ('Vida longa e próspera', 'Vida longa e próspera')], default='Love', max_length=25),
        ),
    ]
