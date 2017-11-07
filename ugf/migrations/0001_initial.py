# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('current_series', models.CharField(max_length=255, choices=[(b'Seed', b'seed'), (b'Pre-Series A', b'pre-series-a'), (b'Series A', b'a'), (b'Series B', b'b'), (b'Series C', b'c'), (b'Series D', b'd'), (b'Exited (acquired)', b'acquired'), (b'Exited (IPO)', b'ipo'), (b'Series E', b'e'), (b'Series F', b'f'), (b'Series G', b'g'), (b'Series H', b'h'), (b'Series J', b'j'), (b'Series I', b'i'), (b'Series I', b'i')])),
                ('last_funding_date', models.DateTimeField()),
                ('last_funding_amount', models.BigIntegerField(default=0.0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Source',
                'verbose_name_plural': 'Sources',
            },
        ),
        migrations.AddField(
            model_name='company',
            name='source',
            field=models.ForeignKey(blank=True, to='ugf.Source', null=True),
        ),
    ]
