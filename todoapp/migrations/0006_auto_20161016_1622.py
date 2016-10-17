# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-16 16:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0005_auto_20161016_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Missed', 'Missed')], default='Pending', max_length=50),
        ),
    ]