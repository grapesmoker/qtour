# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-30 04:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_tournament_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournamentsite',
            name='site_name',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
    ]
