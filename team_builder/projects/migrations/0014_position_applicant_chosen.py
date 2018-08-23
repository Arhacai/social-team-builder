# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-23 16:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0013_auto_20180822_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='applicant_chosen',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='position', to=settings.AUTH_USER_MODEL),
        ),
    ]
