# Generated by Django 3.0.12 on 2021-03-04 08:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0019_auto_20210304_0621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='representation',
            name='compraRepresentation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='representa', to='compras.Compra'),
        ),
    ]
