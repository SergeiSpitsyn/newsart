# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-05-17 00:36
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_auto_20200517_0311'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Комментарий')),
                ('date', models.DateTimeField(db_index=True, default=datetime.datetime(2020, 5, 17, 3, 36, 30, 478111), verbose_name='Добавлен')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'комментарий',
                'verbose_name_plural': 'Комментарии к статьям блога',
                'db_table': 'Comments',
                'ordering': ['-date'],
            },
        ),
        migrations.AddField(
            model_name='blog',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2020, 5, 17, 3, 36, 30, 478111), verbose_name='Опубликовано'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.Blog', verbose_name='Статья'),
        ),
    ]
