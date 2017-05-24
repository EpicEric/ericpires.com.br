# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-24 12:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('telegrambot', '0004_auto_20170523_0226'),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField(blank=True)),
                ('stdin', models.TextField(blank=True)),
                ('chat', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='telegrambot.Chat')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('codename', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='code',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codecompilerbot.Language'),
        ),
    ]