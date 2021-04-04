# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-19 01:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Argument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('value', models.CharField(blank=True, help_text="Valid python code, i.e. strings in 'str'.The variable 'project' contains the project.", max_length=64)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Function',
            fields=[
                ('name', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('doc', models.TextField(blank=True, verbose_name='Description')),
                ('kwargs', models.BooleanField(default=False, verbose_name='Accept any keyword')),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('value', models.CharField(help_text="Valid python code, i.e. strings in 'str'.The variable 'project' contains the project.", max_length=1024)),
            ],
        ),
        migrations.AddField(
            model_name='argument',
            name='function',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Function'),
        ),
    ]