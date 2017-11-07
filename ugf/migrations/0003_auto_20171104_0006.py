# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugf', '0002_auto_20171103_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='last_funding_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
