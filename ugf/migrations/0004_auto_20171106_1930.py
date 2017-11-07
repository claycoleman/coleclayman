# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugf', '0003_auto_20171104_0006'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='domain',
            field=models.URLField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='total_funding',
            field=models.BigIntegerField(default=0.0),
        ),
    ]
