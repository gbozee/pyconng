# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-07-22 18:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0010_ticket_total_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='related',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
