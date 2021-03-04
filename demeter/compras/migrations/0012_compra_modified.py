# Generated by Django 3.0.12 on 2021-03-03 03:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0011_remove_compra_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='modified',
            field=models.DateField(default=datetime.datetime(2021, 3, 3, 3, 36, 36, 966906, tzinfo=utc), verbose_name='Fecha modificacion'),
            preserve_default=False,
        ),
    ]
