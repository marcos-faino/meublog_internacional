# Generated by Django 3.1.7 on 2021-06-01 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meublog', '0002_comentario'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comentario',
            options={'ordering': ('-criado',)},
        ),
    ]
