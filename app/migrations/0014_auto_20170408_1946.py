# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-08 14:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20170408_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cold',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
