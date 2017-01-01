# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimage',
            name='image_file',
            field=models.ImageField(null=True, upload_to=b'image_file', blank=True),
        ),
    ]
