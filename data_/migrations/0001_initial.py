# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-09 01:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seconds', models.FloatField(default=0, null=True, verbose_name='Seconds')),
                ('x_coord', models.FloatField(default=0, null=True, verbose_name='X')),
                ('y_coord', models.FloatField(default=0, null=True, verbose_name='Y')),
                ('z_coord', models.FloatField(default=0, null=True, verbose_name='Z')),
                ('unknown', models.FloatField(default=0, null=True, verbose_name='Unknown')),
                ('temp', models.FloatField(default=0, null=True, verbose_name='Temperature')),
                ('eda', models.FloatField(default=0, null=True, verbose_name='EDA')),
                ('sums', models.FloatField(default=0, null=True, verbose_name='Sum')),
                ('mean', models.FloatField(default=0, null=True, verbose_name='Sum')),
                ('frequency', models.FloatField(default=0, null=True, verbose_name='Sum')),
                ('data_text', models.CharField(max_length=270, verbose_name='Piece of data')),
                ('date_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Trial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('date', models.DateField()),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.AddField(
            model_name='data',
            name='trial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_.Trial', verbose_name='trial this point belongs to'),
        ),
    ]
