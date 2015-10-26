# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Latitude', models.FloatField(null=True, blank=True)),
                ('Longitude', models.FloatField(null=True, blank=True)),
                ('Altitude', models.FloatField(null=True, blank=True)),
                ('Heading', models.FloatField(null=True, blank=True)),
                ('Pitch', models.FloatField(null=True, blank=True)),
                ('Roll', models.FloatField(null=True, blank=True)),
                ('Date', models.DateTimeField(null=True, blank=True)),
                ('Default', models.NullBooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Coordenates',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Latitude', models.FloatField(null=True, blank=True)),
                ('Longitude', models.FloatField(null=True, blank=True)),
                ('Altitude', models.FloatField(null=True, blank=True)),
                ('Extrude', models.FloatField(null=True, blank=True)),
                ('Date', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='InsertDeleteUpdate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('IdObject', models.BigIntegerField(null=True, blank=True)),
                ('UserId', models.BigIntegerField(null=True, blank=True)),
                ('PerformedActivity', models.CharField(max_length=50, null=True, blank=True)),
                ('Date', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MapSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ImageryProvider', models.CharField(max_length=300, null=True, blank=True)),
                ('Url', models.CharField(max_length=300, null=True, blank=True)),
                ('BaseLayerPick', models.NullBooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Objects',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('objectId', models.CharField(max_length=45, null=True, blank=True)),
                ('Type', models.CharField(max_length=50, null=True, blank=True)),
                ('Name', models.CharField(max_length=300, null=True, blank=True)),
                ('Description', models.CharField(max_length=5000, null=True, blank=True)),
                ('url', models.CharField(max_length=100, null=True, blank=True)),
                ('Value', models.FloatField(null=True, blank=True)),
                ('Date', models.DateTimeField(null=True, blank=True)),
                ('Password', models.CharField(max_length=45, null=True, blank=True)),
                ('Floors', models.IntegerField(null=True, blank=True)),
                ('PositionLat', models.FloatField(null=True, blank=True)),
                ('PositionLong', models.FloatField(null=True, blank=True)),
                ('Picture', models.ImageField(null=True, upload_to=b'fotos/%Y/%m/%d', blank=True)),
                ('MaterialImage', models.ImageField(null=True, upload_to=b'fotos/%Y/%m/%d', blank=True)),
                ('MaterialColor', models.CharField(max_length=45, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Servers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Ip', models.CharField(max_length=45, null=True, blank=True)),
                ('UserName', models.CharField(max_length=45, null=True, blank=True)),
                ('Password', models.CharField(max_length=45, null=True, blank=True)),
                ('Port', models.IntegerField(null=True, blank=True)),
                ('Date', models.DateTimeField(null=True, blank=True)),
                ('CodServer', models.ForeignKey(to='campusuhapp.Objects')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(max_length=100)),
                ('UserName', models.CharField(max_length=100, null=True, blank=True)),
                ('Password', models.CharField(max_length=100, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='objects',
            name='UserId',
            field=models.ForeignKey(to='campusuhapp.Users'),
        ),
        migrations.AddField(
            model_name='coordenates',
            name='CodObject',
            field=models.ForeignKey(to='campusuhapp.Objects'),
        ),
        migrations.AddField(
            model_name='camera',
            name='CodObject',
            field=models.ForeignKey(to='campusuhapp.Objects'),
        ),
    ]
