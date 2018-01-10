# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Livro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=255)),
                ('editora', models.CharField(max_length=255)),
                ('isbn', models.CharField(max_length=255)),
                ('isbn2', models.CharField(max_length=255)),
                ('descricao', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('nota', models.CharField(max_length=255)),
                ('paginas', models.CharField(max_length=255)),
                ('edicao', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
