# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-30 09:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20170330_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phase_entry',
            name='date_end',
            field=models.DateField(blank=True, null=True),
        ),
    ]
