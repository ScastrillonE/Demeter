# Generated by Django 3.0.12 on 2021-03-04 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0001_initial'),
        ('ventas', '0006_auto_20210301_1623'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ventas',
            name='kilos',
        ),
        migrations.RemoveField(
            model_name='ventas',
            name='material',
        ),
        migrations.RemoveField(
            model_name='ventas',
            name='unit_value',
        ),
        migrations.CreateModel(
            name='DetVenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kilos', models.CharField(max_length=200, verbose_name='Kilos')),
                ('unit_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materiales.Material')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.Ventas')),
            ],
        ),
    ]
