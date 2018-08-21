# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-20 11:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Constant_type',
            fields=[
                ('constant_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('symbol', models.CharField(max_length=200)),
                ('unit', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Diatomic_constant',
            fields=[
                ('diatomic_constant_id', models.AutoField(primary_key=True, serialize=False)),
                ('value', models.DecimalField(decimal_places=10, max_digits=20)),
                ('delta_plus', models.DecimalField(decimal_places=10, max_digits=20)),
                ('delta_minus', models.DecimalField(decimal_places=10, max_digits=20)),
                ('date_entered', models.DateField(auto_now=True)),
                ('constant_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='data_management.Constant_type')),
            ],
        ),
        migrations.CreateModel(
            name='Molecular_state',
            fields=[
                ('molecular_state_id', models.AutoField(primary_key=True, serialize=False)),
                ('symbol', models.CharField(max_length=200)),
                ('excitation_index', models.CharField(max_length=1)),
                ('total_electronic_spin', models.IntegerField()),
                ('total_angular_momentum', models.IntegerField()),
                ('projected_angular_momentum', models.IntegerField()),
                ('reflection_symmetry', models.CharField(max_length=1)),
                ('parity', models.CharField(blank=True, default='', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Preferred_sets',
            fields=[
                ('preferred_set_id', models.AutoField(primary_key=True, serialize=False)),
                ('constant_type', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='data_management.Constant_type')),
                ('molecular_state', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='data_management.Molecular_state')),
            ],
        ),
        migrations.CreateModel(
            name='Reference_publication',
            fields=[
                ('reference_id', models.AutoField(primary_key=True, serialize=False)),
                ('entry_type', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('journal', models.CharField(max_length=200)),
                ('year', models.IntegerField()),
                ('volume', models.IntegerField()),
                ('doi', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=200)),
                ('number', models.IntegerField()),
                ('pages', models.CharField(max_length=200)),
                ('month', models.IntegerField()),
                ('note', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Source_type',
            fields=[
                ('source_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('source_type', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='User_id',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('uname', models.CharField(max_length=200)),
                ('first', models.CharField(max_length=200)),
                ('last', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='preferred_sets',
            name='reference_publication',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='data_management.Reference_publication'),
        ),
        migrations.AddField(
            model_name='diatomic_constant',
            name='molecular_state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='data_management.Molecular_state'),
        ),
        migrations.AddField(
            model_name='diatomic_constant',
            name='reference_publication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='data_management.Reference_publication'),
        ),
        migrations.AddField(
            model_name='diatomic_constant',
            name='source_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_management.Source_type'),
        ),
        migrations.AddField(
            model_name='diatomic_constant',
            name='user_entered',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='data_management.User_id'),
        ),
    ]