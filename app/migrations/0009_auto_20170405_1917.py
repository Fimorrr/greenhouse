# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-05 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20170405_1912'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='status',
        ),
        migrations.AddField(
            model_name='group',
            name='date_end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Status',
        ),
    ]