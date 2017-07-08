# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendemmia', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bolla',
            name='enopolio',
            field=models.CharField(default=b'1', max_length=25, choices=[(b'1', b'Enopolio di Petrosino'), (b'2', b'Enopolio di Mazara')]),
        ),
    ]
