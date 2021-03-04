# Generated by Django 3.0.12 on 2021-03-03 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0013_auto_20210303_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='creation_date',
            field=models.DateField(blank=True, verbose_name='Fecha creacion'),
        ),
        migrations.AlterField(
            model_name='compra',
            name='modified',
            field=models.DateField(blank=True, verbose_name='Fecha modificacion'),
        ),
        migrations.AlterField(
            model_name='detcompra',
            name='creation_date',
            field=models.DateField(blank=True, verbose_name='Fecha creacion'),
        ),
        migrations.AlterField(
            model_name='detcompra',
            name='modified',
            field=models.DateField(blank=True, verbose_name='Fecha modificacion'),
        ),
    ]