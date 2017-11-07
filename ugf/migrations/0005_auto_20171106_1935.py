# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugf', '0004_auto_20171106_1930'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='domain',
        ),
        migrations.AddField(
            model_name='company',
            name='retrieved_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
