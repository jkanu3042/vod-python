# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-13 11:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20170713_2018'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='tag_get',
            new_name='tag_set',
        ),
    ]
