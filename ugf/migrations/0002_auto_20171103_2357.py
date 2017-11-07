# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugf', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='date_updated',
        ),
        migrations.AddField(
            model_name='company',
            name='data_retrieved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='company',
            name='date_data_retrieved',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='valid_candidate',
            field=models.BooleanField(default=True),
        ),
    ]
