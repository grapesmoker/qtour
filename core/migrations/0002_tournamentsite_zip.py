# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-30 03:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournamentsite',
            name='zip',
            field=models.CharField(default=None, max_length=5),
            preserve_default=False,
        ),
    ]
