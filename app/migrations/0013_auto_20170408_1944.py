# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-08 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20170408_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cold',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='heat',
            name='date',
            field=models.DateField(),
        ),
    ]
