# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-26 14:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0002_auto_20160625_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='commit',
            name='description',
            field=models.TextField(default=None, verbose_name='评论'),
            preserve_default=False,
        ),
    ]