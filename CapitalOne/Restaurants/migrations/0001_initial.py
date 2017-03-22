# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-03-19 21:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('locationX', models.DecimalField(decimal_places=9, max_digits=12)),
                ('locationY', models.DecimalField(decimal_places=9, max_digits=12)),
                ('cost', models.IntegerField()),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('picture', models.CharField(max_length=2000)),
            ],
        ),
    ]