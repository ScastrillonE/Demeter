# Generated by Django 3.0.12 on 2021-03-04 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0009_auto_20210304_1839'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ventas',
            old_name='create',
            new_name='creation_date',
        ),
    ]
