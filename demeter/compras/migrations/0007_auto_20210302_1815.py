# Generated by Django 3.0.12 on 2021-03-02 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0006_auto_20210228_1415'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compra',
            name='active',
        ),
        migrations.RemoveField(
            model_name='compra',
            name='bonus',
        ),
        migrations.RemoveField(
            model_name='compra',
            name='kilos',
        ),
        migrations.RemoveField(
            model_name='compra',
            name='material',
        ),
        migrations.RemoveField(
            model_name='compra',
            name='modified',
        ),
        migrations.RemoveField(
            model_name='compra',
            name='unit_value',
        ),
        migrations.CreateModel(
            name='DetCompra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(max_length=150, verbose_name='Nombre material')),
                ('kilos', models.CharField(max_length=160, verbose_name='Kilos')),
                ('unit_value', models.CharField(max_length=160, verbose_name='Valor unitario')),
                ('creation_date', models.DateField(verbose_name='Fecha creacion')),
                ('modified', models.DateField(verbose_name='Fecha modificacion')),
                ('active', models.BooleanField(default=True)),
                ('bonus', models.CharField(choices=[('No_aplica', 'No aplica'), ('Carton', 'Carton'), ('Archivo', 'Archivo'), ('Periodico', 'Periodico'), ('Plega', 'Plega'), ('Plastico', 'Plastico'), ('Chatarra', 'Chatarra'), ('Vidrio', 'Vidrio'), ('Otros', 'Otros')], default='No_aplica', max_length=100)),
                ('compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compras.Compra')),
            ],
        ),
    ]
