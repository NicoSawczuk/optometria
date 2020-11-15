# Generated by Django 3.1.3 on 2020-11-12 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20201112_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='medico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.medico', verbose_name='Medico'),
        ),
        migrations.AlterField(
            model_name='turno',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.paciente', verbose_name='Paciente'),
        ),
    ]