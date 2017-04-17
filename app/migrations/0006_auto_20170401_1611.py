# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-01 11:11
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20170330_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='count',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000)]),
        ),
        migrations.AlterField(
            model_name='plant',
            name='square',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.1), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='room',
            name='length',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.1), django.core.validators.MaxValueValidator(1000)]),
        ),
        migrations.AlterField(
            model_name='room',
            name='width',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.1), django.core.validators.MaxValueValidator(1000)]),
        ),
    ]
