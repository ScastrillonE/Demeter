# Generated by Django 3.0.12 on 2021-03-03 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0009_auto_20210303_0334'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='modified',
            field=models.DateField(default=0, verbose_name='Fecha modificacion'),
            preserve_default=False,
        ),
    ]
