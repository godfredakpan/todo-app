# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-12 15:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0002_auto_20161012_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
