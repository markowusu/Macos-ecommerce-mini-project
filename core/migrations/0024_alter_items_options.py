# Generated by Django 3.2.3 on 2021-11-04 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_alter_items_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='items',
            options={'ordering': ['-price']},
        ),
    ]