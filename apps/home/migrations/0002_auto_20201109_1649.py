# Generated by Django 3.1.3 on 2020-11-09 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medico',
            name='fecha_nac',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='fecha_nac',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
