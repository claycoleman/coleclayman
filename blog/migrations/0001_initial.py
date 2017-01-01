# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField(null=True, verbose_name=b'comment body', blank=True)),
                ('author', models.CharField(max_length=255, null=True, blank=True)),
                ('date_posted', models.DateTimeField(auto_now_add=True, null=True)),
                ('parent_comment', models.ForeignKey(blank=True, to='blog.Comment', null=True)),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('published', models.BooleanField(default=False)),
                ('title', models.TextField(null=True, blank=True)),
                ('body', models.TextField(null=True, blank=True)),
                ('preview_image', models.ImageField(null=True, upload_to=b'previews', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('posted', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('image_file', models.ImageField(null=True, upload_to=b'previews', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(blank=True, to='blog.Post', null=True),
        ),
    ]
