# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20161231_2010'),
    ]

    operations = [
        migrations.CreateModel(
            name='UniqueVisitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('session_id', models.CharField(max_length=255, null=True, blank=True)),
                ('date_visited', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='number_of_hits',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='uniquevisitor',
            name='post',
            field=models.ForeignKey(blank=True, to='blog.Post', null=True),
        ),
    ]
