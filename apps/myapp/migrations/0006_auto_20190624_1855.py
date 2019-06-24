# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-24 18:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20190624_1840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='liked_by',
        ),
        migrations.RemoveField(
            model_name='like',
            name='quote_liked',
        ),
        migrations.RenameField(
            model_name='quote',
            old_name='user_who_liked',
            new_name='users_who_liked',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
