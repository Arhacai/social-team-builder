# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-18 14:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_auto_20180818_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications_position', to='projects.Position'),
        ),
        migrations.AlterField(
            model_name='position',
            name='applications',
            field=models.ManyToManyField(blank=True, related_name='position_applications', to='projects.Application'),
        ),
    ]