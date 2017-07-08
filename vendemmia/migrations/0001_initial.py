# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import vendemmia.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='bolla',
            fields=[
                ('idbolla', models.AutoField(serialize=False, primary_key=True)),
                ('num', models.PositiveIntegerField()),
                ('data', models.DateField(default=vendemmia.models.ultimovalore)),
                ('diraspata', models.BooleanField(default=False)),
                ('grado', models.DecimalField(max_digits=4, decimal_places=2)),
                ('netto', models.DecimalField(max_digits=5, decimal_places=2)),
                ('note', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Bollette',
            },
        ),
        migrations.CreateModel(
            name='cultivar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Cultivar',
            },
        ),
        migrations.CreateModel(
            name='provenienza',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['nome'],
                'verbose_name_plural': 'Provenienza',
            },
        ),
        migrations.CreateModel(
            name='provenienza_dettaglio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('percentuale', models.PositiveSmallIntegerField(default=100)),
                ('bolla', models.ForeignKey(to='vendemmia.bolla')),
            ],
            options={
                'verbose_name_plural': 'Provenienze dettagliate',
            },
        ),
        migrations.CreateModel(
            name='provenienza_eff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=50)),
                ('biologico', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['nome'],
                'verbose_name_plural': 'Provenienze dettagliate',
            },
        ),
        migrations.CreateModel(
            name='qualita',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Qualit\xe0',
            },
        ),
        migrations.CreateModel(
            name='ven',
            fields=[
                ('anno', models.PositiveSmallIntegerField(default=2016, serialize=False, primary_key=True)),
                ('inizio', models.DateField()),
                ('fine', models.DateField(blank=True)),
                ('note', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Vendemmie',
            },
        ),
        migrations.AddField(
            model_name='provenienza_dettaglio',
            name='provenienza_eff',
            field=models.ForeignKey(to='vendemmia.provenienza_eff'),
        ),
        migrations.AddField(
            model_name='bolla',
            name='Cultivar',
            field=models.ForeignKey(related_name='Cultivar', to='vendemmia.cultivar'),
        ),
        migrations.AddField(
            model_name='bolla',
            name='Cultivar_eff',
            field=models.ForeignKey(related_name='Cultivar_eff', to='vendemmia.cultivar'),
        ),
        migrations.AddField(
            model_name='bolla',
            name='Provenienza',
            field=models.ForeignKey(to='vendemmia.provenienza'),
        ),
        migrations.AddField(
            model_name='bolla',
            name='Provenienza_eff',
            field=models.ManyToManyField(related_name='Provenienza_eff', through='vendemmia.provenienza_dettaglio', to='vendemmia.provenienza_eff'),
        ),
        migrations.AddField(
            model_name='bolla',
            name='Qualita',
            field=models.ForeignKey(to='vendemmia.qualita'),
        ),
        migrations.AddField(
            model_name='bolla',
            name='Vendemmia',
            field=models.ForeignKey(default=vendemmia.models.ultimavendemmia, to='vendemmia.ven'),
        ),
    ]
