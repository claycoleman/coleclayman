# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20161231_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='uniquevisitor',
            name='number_of_hits',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
