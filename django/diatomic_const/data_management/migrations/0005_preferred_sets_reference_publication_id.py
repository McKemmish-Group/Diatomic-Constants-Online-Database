# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-06 16:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_management', '0004_remove_preferred_sets_reference_publication'),
    ]

    operations = [
        migrations.AddField(
            model_name='preferred_sets',
            name='reference_publication_id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='data_management.Reference_publication'),
        ),
    ]
