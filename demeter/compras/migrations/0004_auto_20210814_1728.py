# Generated by Django 3.0.12 on 2021-08-14 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0003_merge_20210310_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detcompra',
            name='unit_value',
            field=models.IntegerField(default=0),
        ),
    ]