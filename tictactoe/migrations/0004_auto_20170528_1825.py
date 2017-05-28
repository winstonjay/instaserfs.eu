# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-28 18:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tictactoe', '0003_counter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counter',
            name='title',
            field=models.CharField(choices=[('COMPUTER', 'computer'), ('DRAWS', 'draws'), ('HUMANS', 'humans')], max_length=30),
        ),
    ]
