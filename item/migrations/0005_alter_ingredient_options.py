# Generated by Django 5.0.4 on 2024-05-01 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0004_ingredient'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['name'], 'verbose_name_plural': 'Ingredients'},
        ),
    ]