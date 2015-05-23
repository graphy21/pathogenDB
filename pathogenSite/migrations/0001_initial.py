# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlastLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('execution_date', models.DateTimeField(verbose_name=b'blast execution date')),
            ],
        ),
        migrations.CreateModel(
            name='BlastResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField()),
                ('attachment', models.FileField(upload_to=b'blast_results')),
            ],
        ),
        migrations.CreateModel(
            name='FastaFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('attachment', models.FileField(upload_to=b'fasta_files')),
            ],
        ),
        migrations.AddField(
            model_name='blastlog',
            name='blast_result',
            field=models.ForeignKey(to='pathogenSite.BlastResult'),
        ),
    ]
