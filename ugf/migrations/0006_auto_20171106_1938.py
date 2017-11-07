# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugf', '0005_auto_20171106_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='current_series',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
