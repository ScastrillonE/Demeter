# Generated by Django 3.0.12 on 2021-02-26 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compra',
            name='client_name',
        ),
        migrations.AddField(
            model_name='compra',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
