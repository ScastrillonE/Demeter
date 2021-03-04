# Generated by Django 3.0.12 on 2021-03-04 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0007_auto_20210304_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='ventas',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.CreateModel(
            name='Representation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('representation', models.CharField(blank=True, max_length=999, null=True)),
                ('ventaRepresentation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='representa', to='ventas.Ventas')),
            ],
        ),
    ]